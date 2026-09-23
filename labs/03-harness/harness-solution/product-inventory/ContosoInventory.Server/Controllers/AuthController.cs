using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using ContosoInventory.Shared.DTOs;

namespace ContosoInventory.Server.Controllers;

/// <summary>
/// Handles user authentication operations.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly SignInManager<IdentityUser> _signInManager;
    private readonly UserManager<IdentityUser> _userManager;
    private readonly ILogger<AuthController> _logger;

    public AuthController(
        SignInManager<IdentityUser> signInManager,
        UserManager<IdentityUser> userManager,
        ILogger<AuthController> logger)
    {
        _signInManager = signInManager;
        _userManager = userManager;
        _logger = logger;
    }

    /// <summary>
    /// Authenticates a user and sets the auth cookie.
    /// </summary>
    /// <param name="loginDto">The login credentials.</param>
    /// <returns>The authenticated user's information.</returns>
    [HttpPost("login")]
    [AllowAnonymous]
    [ProducesResponseType(typeof(UserInfoDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> Login([FromBody] LoginDto loginDto)
    {
        // Enforce uniform response time to prevent user enumeration via timing analysis
        var stopwatch = System.Diagnostics.Stopwatch.StartNew();
        try
        {
            _logger.LogInformation("Login attempt for {Email}.", loginDto.Email);

            var result = await _signInManager.PasswordSignInAsync(
                loginDto.Email,
                loginDto.Password,
                isPersistent: false,
                lockoutOnFailure: true);

            if (result.Succeeded)
            {
                var user = await _userManager.FindByEmailAsync(loginDto.Email);
                if (user == null)
                {
                    return Unauthorized(new { message = "Invalid email or password." });
                }

                var userInfo = await GetUserInfoAsync(user);
                _logger.LogInformation("User {Email} logged in successfully.", loginDto.Email);
                return Ok(userInfo);
            }

            if (result.IsLockedOut)
            {
                _logger.LogWarning("Account locked out for {Email}.", loginDto.Email);
                return Unauthorized(new { message = "Account is temporarily locked. Please try again later." });
            }

            _logger.LogWarning("Failed login attempt for {Email}.", loginDto.Email);
            return Unauthorized(new { message = "Invalid email or password." });
        }
        finally
        {
            // Ensure minimum 1-second response time for all outcomes (success and failure)
            // to prevent user enumeration via timing side-channel analysis
            var elapsed = stopwatch.ElapsedMilliseconds;
            var remaining = 1000 - (int)elapsed;
            if (remaining > 0)
            {
                await Task.Delay(remaining);
            }
        }
    }

    /// <summary>
    /// Signs the user out and clears the auth cookie.
    /// </summary>
    /// <returns>A success message.</returns>
    [HttpPost("logout")]
    [Authorize]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<IActionResult> Logout()
    {
        await _signInManager.SignOutAsync();
        _logger.LogInformation("User logged out.");
        return Ok(new { message = "Logged out successfully." });
    }

    /// <summary>
    /// Returns the current authenticated user's information.
    /// </summary>
    /// <returns>The current user's information.</returns>
    [HttpGet("me")]
    [Authorize]
    [ProducesResponseType(typeof(UserInfoDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<IActionResult> GetCurrentUser()
    {
        var user = await _userManager.GetUserAsync(User);
        if (user == null)
        {
            return Unauthorized();
        }

        var userInfo = await GetUserInfoAsync(user);
        return Ok(userInfo);
    }

    private async Task<UserInfoDto> GetUserInfoAsync(IdentityUser user)
    {
        var roles = await _userManager.GetRolesAsync(user);
        var claims = await _userManager.GetClaimsAsync(user);
        var displayName = claims.FirstOrDefault(c => c.Type == "DisplayName")?.Value ?? user.Email ?? string.Empty;

        return new UserInfoDto
        {
            Email = user.Email ?? string.Empty,
            DisplayName = displayName,
            Role = roles.FirstOrDefault() ?? string.Empty
        };
    }
}
