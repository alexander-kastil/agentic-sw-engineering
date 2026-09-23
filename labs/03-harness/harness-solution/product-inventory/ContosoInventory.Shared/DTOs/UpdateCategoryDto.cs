namespace ContosoInventory.Shared.DTOs;

public class UpdateCategoryDto
{
    [Required]
    [StringLength(100, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [StringLength(500)]
    public string Description { get; set; } = string.Empty;

    [Range(1, 1000)]
    public int DisplayOrder { get; set; }

    public bool IsActive { get; set; }
}
