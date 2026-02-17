public static class Validator
{
    public static bool IsPalindrome(string input)
    {
        char[] charArray = input.ToCharArray();
        Array.Reverse(charArray);
        string reversedInput = new string(charArray);
        if (input == reversedInput)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}