public class Validator
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

    // check if the input is even
    public static bool IsEven(int input)
    {
        if (input % 2 == 0)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    // get a count of the items in a string array. use a for to loop through the array
    public static int GetTotal(int[] input)
    {
        int total = 0;
        for (int i = 0; i < input.Length; i++)
        {
            total += input[i];
        }
        return total;
    }
}