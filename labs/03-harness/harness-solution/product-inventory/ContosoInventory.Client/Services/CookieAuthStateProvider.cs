using System.Net.Http.Json;
using System.Security.Claims;
using Microsoft.AspNetCore.Components.Authorization;
using ContosoInventory.Shared.DTOs;

namespace ContosoInventory.Client.Services;

public class CookieAuthStateProvider : AuthenticationStateProvider
{
    private readonly HttpClient _httpClient;
    private UserInfoDto? _cachedUser;
    private bool _isInitialized;

    public CookieAuthStateProvider(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public override async Task<AuthenticationState> GetAuthenticationStateAsync()
    {
        if (!_isInitialized)
        {
            _cachedUser = await FetchUserInfoAsync();
            _isInitialized = true;
        }

        return CreateAuthState(_cachedUser);
    }

    public async Task<UserInfoDto?> LoginAsync(LoginDto loginDto)
    {
        var response = await _httpClient.PostAsJsonAsync("/api/auth/login", loginDto);

        if (response.IsSuccessStatusCode)
        {
            var userInfo = await response.Content.ReadFromJsonAsync<UserInfoDto>();
            _cachedUser = userInfo;
            NotifyAuthenticationStateChanged(Task.FromResult(CreateAuthState(_cachedUser)));
            return userInfo;
        }

        return null;
    }

    public async Task LogoutAsync()
    {
        await _httpClient.PostAsync("/api/auth/logout", null);
        _cachedUser = null;
        NotifyAuthenticationStateChanged(Task.FromResult(CreateAuthState(null)));
    }

    public void InvalidateCache()
    {
        _cachedUser = null;
        _isInitialized = false;
        NotifyAuthenticationStateChanged(GetAuthenticationStateAsync());
    }

    private async Task<UserInfoDto?> FetchUserInfoAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync("/api/auth/me");
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadFromJsonAsync<UserInfoDto>();
            }
        }
        catch
        {
            // Not authenticated
        }

        return null;
    }

    private static AuthenticationState CreateAuthState(UserInfoDto? user)
    {
        if (user == null)
        {
            return new AuthenticationState(new ClaimsPrincipal(new ClaimsIdentity()));
        }

        var claims = new List<Claim>
        {
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Name, user.DisplayName),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var identity = new ClaimsIdentity(claims, "cookie");
        return new AuthenticationState(new ClaimsPrincipal(identity));
    }
}
