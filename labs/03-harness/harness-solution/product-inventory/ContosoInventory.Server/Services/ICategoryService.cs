using ContosoInventory.Shared.DTOs;

namespace ContosoInventory.Server.Services;

/// <summary>
/// Defines operations for managing inventory categories.
/// </summary>
public interface ICategoryService
{
    /// <summary>
    /// Retrieves all categories ordered by display order.
    /// </summary>
    Task<List<CategoryResponseDto>> GetAllCategoriesAsync();

    /// <summary>
    /// Retrieves a category by its unique identifier.
    /// </summary>
    /// <param name="id">The category identifier.</param>
    /// <returns>The category DTO, or null if not found.</returns>
    Task<CategoryResponseDto?> GetCategoryByIdAsync(int id);

    /// <summary>
    /// Creates a new category.
    /// </summary>
    /// <param name="dto">The category creation data.</param>
    /// <returns>The created category DTO.</returns>
    /// <exception cref="InvalidOperationException">Thrown when a category with the same name already exists.</exception>
    Task<CategoryResponseDto> CreateCategoryAsync(CreateCategoryDto dto);

    /// <summary>
    /// Updates an existing category.
    /// </summary>
    /// <param name="id">The category identifier.</param>
    /// <param name="dto">The updated category data.</param>
    /// <returns>The updated category DTO, or null if not found.</returns>
    /// <exception cref="InvalidOperationException">Thrown when a category with the same name already exists.</exception>
    Task<CategoryResponseDto?> UpdateCategoryAsync(int id, UpdateCategoryDto dto);

    /// <summary>
    /// Deletes a category by its unique identifier.
    /// </summary>
    /// <param name="id">The category identifier.</param>
    /// <returns>True if the category was deleted, false if not found.</returns>
    Task<bool> DeleteCategoryAsync(int id);

    /// <summary>
    /// Toggles the active status of a category.
    /// </summary>
    /// <param name="id">The category identifier.</param>
    /// <returns>The updated category DTO, or null if not found.</returns>
    Task<CategoryResponseDto?> ToggleActiveAsync(int id);
}
