namespace ContosoInventory.Shared.DTOs;

public class RestockProductDto
{
    [Range(1, int.MaxValue)]
    public int Quantity { get; set; }
}
