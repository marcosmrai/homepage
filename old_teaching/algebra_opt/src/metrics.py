from typing import Literal
import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt

# Enable 64-bit precision in JAX for accurate numerical computations
jax.config.update("jax_enable_x64", True)

# Type alias for JAX array
Vector = jax.Array

def compute_norm(x: Vector, p: Literal["l1", "l2", "linf"] = "l2") -> float:
    """Calculates L1, L2, or L-infinity norm of a vector x using JAX.
    
    Args:
        x: Input JAX array vector.
        p: Type of norm to compute ('l1', 'l2', or 'linf').
        
    Returns:
        Scalar float representing the computed norm.
    """
    if p == "l1":
        return float(jnp.sum(jnp.abs(x)))
    elif p == "l2":
        return float(jnp.sqrt(jnp.sum(x ** 2)))
    elif p == "linf":
        return float(jnp.max(jnp.abs(x)))
    raise ValueError(f"Unsupported norm type: {p}")

def inner_product(u: Vector, v: Vector) -> float:
    """Calculates the inner product between two vectors using JAX.
    
    Args:
        u: First input vector.
        v: Second input vector.
        
    Returns:
        Scalar float value of the inner product.
    """
    return float(jnp.dot(u, v))

def cosine_distance(u: Vector, v: Vector) -> float:
    """Calculates cosine distance: 1 - cos(theta) using JAX.
    
    Args:
        u: First input vector.
        v: Second input vector.
        
    Returns:
        Scalar float cosine distance.
    """
    norm_u = compute_norm(u, p="l2")
    norm_v = compute_norm(v, p="l2")
    
    # Avoid division by zero
    is_zero = (norm_u == 0.0) | (norm_v == 0.0)
    similarity = jnp.where(is_zero, 0.0, inner_product(u, v) / (norm_u * norm_v))
    
    return float(1.0 - similarity)

def custom_knn_search(
    query: Vector,
    dataset: Vector,
    k: int,
    p: Literal["l1", "l2", "linf"] = "l2"
) -> tuple[Vector, Vector]:
    """Vectorized k-NN search using JAX vmap over dataset samples.
    
    Args:
        query: Query vector of shape (d,).
        dataset: Matrix of shape (N, d) containing dataset samples.
        k: Number of nearest neighbors to retrieve.
        p: Norm type to evaluate distances.
        
    Returns:
        Tuple containing:
            - Array of top-k indices.
            - Array of top-k distances.
    """
    # Vectorize pairwise norm calculation over axis 0 of dataset
    diffs = dataset - query
    
    if p == "l1":
        distances = jnp.sum(jnp.abs(diffs), axis=1)
    elif p == "l2":
        distances = jnp.sqrt(jnp.sum(diffs ** 2, axis=1))
    elif p == "linf":
        distances = jnp.max(jnp.abs(diffs), axis=1)
    else:
        raise ValueError(f"Unsupported norm type: {p}")

    # Retrieve top-k smallest distances and indices
    idx_sorted = jnp.argsort(distances)[:k]
    return idx_sorted, distances[idx_sorted]

def plot_unit_balls() -> plt.Figure:
    """Generates a comparison plot of unit balls for L1, L2, and L-infinity norms using JAX.
    
    Returns:
        Matplotlib figure instance.
    """
    angles = jnp.linspace(0, 2 * jnp.pi, 400)
    circle_pts = jnp.stack([jnp.cos(angles), jnp.sin(angles)], axis=1)

    fig, ax = plt.subplots(figsize=(5, 5))

    # L2 Unit Circle
    ax.plot(circle_pts[:, 0], circle_pts[:, 1], label=r'$L_2$ (Euclidean)', color='blue')

    # L1 Unit Diamond
    l1_pts = circle_pts / jnp.sum(jnp.abs(circle_pts), axis=1, keepdims=True)
    ax.plot(l1_pts[:, 0], l1_pts[:, 1], label=r'$L_1$ (Manhattan)', color='red')

    # L-infinity Unit Square
    linf_pts = circle_pts / jnp.max(jnp.abs(circle_pts), axis=1, keepdims=True)
    ax.plot(linf_pts[:, 0], linf_pts[:, 1], label=r'$L_\infty$ (Chebyshev)', color='green')

    ax.set_aspect('equal')
    ax.grid(True, linestyle='--')
    ax.legend()
    plt.title("Unit Balls Comparison in R² (JAX)")
    return fig