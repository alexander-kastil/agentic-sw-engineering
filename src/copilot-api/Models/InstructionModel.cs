namespace CopilotApi.Models;

public class InstructionModel(string name, string description)
{
    public string Name { get; } = name;
    public string Description { get; } = description;
}
