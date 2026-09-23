using System.Net.Http.Json;
using ContosoInventory.Shared.DTOs;

namespace ContosoInventory.Client.Services;

public class CategoryApiService
{
    private readonly HttpClient _httpClient;

    public CategoryApiService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<List<CategoryResponseDto>> GetAllCategoriesAsync()
    {
        var response = await _httpClient.GetAsync("/api/categories");
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<List<CategoryResponseDto>>() ?? new();
    }

    public async Task<CategoryResponseDto?> GetCategoryByIdAsync(int id)
    {
        var response = await _httpClient.GetAsync($"/api/categories/{id}");
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadFromJsonAsync<CategoryResponseDto>();
        }
        return null;
    }

    public async Task<CategoryResponseDto?> CreateCategoryAsync(CreateCategoryDto dto)
    {
        var response = await _httpClient.PostAsJsonAsync("/api/categories", dto);
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadFromJsonAsync<CategoryResponseDto>();
        }
        var error = await response.Content.ReadAsStringAsync();
        throw new HttpRequestException(error);
    }

    public async Task<CategoryResponseDto?> UpdateCategoryAsync(int id, UpdateCategoryDto dto)
    {
        var response = await _httpClient.PutAsJsonAsync($"/api/categories/{id}", dto);
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadFromJsonAsync<CategoryResponseDto>();
        }
        var error = await response.Content.ReadAsStringAsync();
        throw new HttpRequestException(error);
    }

    public async Task<bool> DeleteCategoryAsync(int id)
    {
        var response = await _httpClient.DeleteAsync($"/api/categories/{id}");
        return response.IsSuccessStatusCode;
    }

    public async Task<CategoryResponseDto?> ToggleActiveAsync(int id)
    {
        var response = await _httpClient.PostAsync($"/api/categories/{id}/toggle-active", null);
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadFromJsonAsync<CategoryResponseDto>();
        }
        return null;
    }
}
