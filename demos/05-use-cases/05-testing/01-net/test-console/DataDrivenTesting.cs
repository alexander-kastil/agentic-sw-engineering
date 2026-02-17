using System;
using Xunit;

public class DataDrivenTests
{
    [Theory]
    [MemberData(nameof(GetTotalTestData))]
    public void GetTotal_ShouldReturnCorrectTotal(int[] input, int expected)
    {
        var result = Validator.GetTotal(input);
        Assert.Equal(expected, result);
    }

    public static IEnumerable<object[]> GetTotalTestData => new List<object[]>
    {
        new object[] { new int[] { 1, 2, 3 }, 6 },
        new object[] { new int[] { -1, -2, -3 }, -6 },
        new object[] { new int[] { 0, 0, 0 }, 0 },
        new object[] { new int[] { 100, 200, 300 }, 600 },
        new object[] { new int[] { }, 0 },
    };
}