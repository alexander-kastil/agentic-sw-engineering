# .NET Core Testing

Scaffold project:

```bash
@workspace /new create a dotnet console app including xunit tests. add a Validator class that hast one static method that checks if a string is a Palindrome and returns a boolean
```

Run it, notice possible problems, and create it manually and setup testing

```bash
add nugget packages xunit and .net testing
```

Fix the entry function

```bash
/fix optimize the string to be checked, introduce a variable
```

Add validator, add methods to check for even ad to get a count from an array:

```c#
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
```

- Generate tests for the validator

```bash
@workspace /new create a test class for the Validator class. add a test for the IsPalindrome method
```

- Generate test data for data driven testing

```bash
@workspace Generate test data for the GetTotal method which can be used for data driven testing
```

```bash
@workspace Generate test data for the GetTotal method which can be used for data driven testing including nulls and empty arrays    
```