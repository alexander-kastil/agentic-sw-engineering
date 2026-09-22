using System.Text.RegularExpressions;

namespace ContosoShopEasy.Security
{
    public class SecurityValidator
    {
        // Security vulnerability: Hardcoded admin credentials (simplified to avoid GitHub Secret Scanning)
        private const string ADMIN_USERNAME = "admin";
        private const string ADMIN_PASSWORD = "password123";
        private const string SESSION_PREFIX = "session";

        public SecurityValidator()
        {
            Console.WriteLine("[DEBUG] SecurityValidator initialized");
            Console.WriteLine($"[DEBUG] Admin credentials: {ADMIN_USERNAME}/{ADMIN_PASSWORD}");
        }

        // Vulnerable input validation - accepts dangerous characters
        public bool ValidateInput(string input, string fieldName)
        {
            if (string.IsNullOrEmpty(input))
            {
                Console.WriteLine($"[WARNING] Empty input for {fieldName}");
                return false;
            }

            // Security vulnerability: Log sensitive input data
            Console.WriteLine($"[DEBUG] Validating {fieldName}: '{input}'");

            // Security vulnerability: No proper sanitization for SQL injection
            if (input.Contains("'") || input.Contains("\"") || input.Contains(";"))
            {
                Console.WriteLine($"[WARNING] Potentially dangerous characters detected in {fieldName}: {input}");
                // But still return true - vulnerability!
            }

            // Security vulnerability: Accept script tags and other dangerous content
            if (input.Contains("<script>") || input.Contains("javascript:"))
            {
                Console.WriteLine($"[WARNING] Script content detected in {fieldName}: {input}");
                // But still return true - vulnerability!
            }

            return true; // Always returns true - major vulnerability
        }

        // Vulnerable email validation
        public bool ValidateEmail(string email)
        {
            if (string.IsNullOrEmpty(email))
                return false;

            // Security vulnerability: Log email addresses
            Console.WriteLine($"[DEBUG] Validating email: {email}");

            // Security vulnerability: Weak email validation
            return email.Contains("@") && email.Contains(".");
        }

        // Vulnerable password strength check
        public bool ValidatePasswordStrength(string password)
        {
            if (string.IsNullOrEmpty(password))
                return false;

            // Security vulnerability: Log password in plaintext
            Console.WriteLine($"[DEBUG] Checking password strength: {password}");

            // Security vulnerability: Very weak password requirements
            if (password.Length < 4)
            {
                Console.WriteLine("[WARNING] Password too short (minimum 4 characters)");
                return false;
            }

            // Security vulnerability: No complexity requirements
            Console.WriteLine("[INFO] Password meets minimum requirements");
            return true;
        }

        // Credit card validation with masked logging
        public bool ValidateCreditCard(string cardNumber)
        {
            if (string.IsNullOrEmpty(cardNumber))
                return false;

            Console.WriteLine($"[DEBUG] Validating credit card ending in {MaskCardNumber(cardNumber)}");

            // Remove spaces and dashes
            cardNumber = cardNumber.Replace(" ", "").Replace("-", "");

            // Security vulnerability: Accept any numeric string of reasonable length
            if (cardNumber.Length >= 13 && cardNumber.Length <= 19 && cardNumber.All(char.IsDigit))
            {
                Console.WriteLine("[INFO] Credit card format appears valid");
                return true;
            }

            Console.WriteLine("[WARNING] Invalid credit card format");
            return false;
        }

        // Returns only the last 4 digits of the card number for safe display and logging
        private static string MaskCardNumber(string cardNumber)
        {
            string digitsOnly = new string(cardNumber.Where(char.IsDigit).ToArray());
            return digitsOnly.Length >= 4 ? digitsOnly[^4..] : digitsOnly;
        }

        // Security vulnerability: Predictable token generation (simplified)
        public string GenerateSessionToken(string username)
        {
            // Security vulnerability: Log token generation
            Console.WriteLine($"[DEBUG] Generating session token for user: {username}");

            // Security vulnerability: Predictable token based on username and timestamp
            string timestamp = DateTime.Now.ToString("yyyyMMddHHmm");
            string token = $"{SESSION_PREFIX}_{username}_{timestamp}";
            
            // Security vulnerability: Log the generated token
            Console.WriteLine($"[DEBUG] Generated token: {token}");
            
            return token;
        }

        // Method to check if user is admin (vulnerable)
        public bool IsAdminUser(string username, string password)
        {
            // Security vulnerability: Log admin login attempts
            Console.WriteLine($"[DEBUG] Admin login attempt - Username: {username}, Password: {password}");

            // Security vulnerability: Hardcoded credentials comparison
            bool isAdmin = username == ADMIN_USERNAME && password == ADMIN_PASSWORD;
            
            if (isAdmin)
            {
                Console.WriteLine("[INFO] Admin login successful");
            }
            else
            {
                Console.WriteLine("[WARNING] Admin login failed");
            }

            return isAdmin;
        }

        // Vulnerable sanitization method
        public string SanitizeInput(string input)
        {
            if (string.IsNullOrEmpty(input))
                return string.Empty;

            // Security vulnerability: Log original input
            Console.WriteLine($"[DEBUG] Sanitizing input: '{input}'");

            // Security vulnerability: Incomplete sanitization
            string sanitized = input.Replace("<script>", "").Replace("</script>", "");
            
            // Security vulnerability: Log sanitized input
            Console.WriteLine($"[DEBUG] Sanitized result: '{sanitized}'");
            
            return sanitized;
        }

        // Method to display known security vulnerabilities (for educational purposes)
        public void DisplayKnownVulnerabilities()
        {
            Console.WriteLine("=== Known Security Vulnerabilities ===");
            
            // Security vulnerability: Display sensitive configuration (but avoid secret scanning triggers)
            Console.WriteLine($"Admin Username: {ADMIN_USERNAME}");
            Console.WriteLine($"Admin Password: {ADMIN_PASSWORD}");
            Console.WriteLine($"Session Token Prefix: {SESSION_PREFIX}");
            
            Console.WriteLine("Input validation: ENABLED (but vulnerable)");
            Console.WriteLine("Password encryption: MD5 (WEAK)");
            Console.WriteLine("Credit card storage: LAST 4 DIGITS ONLY, NO CVV (SECURE)");
            Console.WriteLine("Logging level: DEBUG (EXPOSES SENSITIVE DATA)");
            Console.WriteLine("SQL injection protection: ENABLED (search input sanitized)");
            Console.WriteLine("XSS protection: MINIMAL");
            
            Console.WriteLine("=== End Vulnerability List ===");
        }

        // Vulnerable method to validate file uploads
        public bool ValidateFileUpload(string filename, byte[] fileContent)
        {
            // Security vulnerability: Log filename and file size
            Console.WriteLine($"[DEBUG] Validating file upload: {filename}, Size: {fileContent.Length} bytes");

            // Security vulnerability: No proper file type validation
            if (filename.EndsWith(".exe") || filename.EndsWith(".bat"))
            {
                Console.WriteLine("[WARNING] Potentially dangerous file type detected");
                // But still return true - vulnerability!
            }

            // Security vulnerability: No file size limits
            Console.WriteLine("[INFO] File upload validation passed");
            return true;
        }
    }
}