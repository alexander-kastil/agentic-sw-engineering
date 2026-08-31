using CopilotApi.Models;
using Microsoft.AspNetCore.Mvc;

namespace CopilotApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class InstructionsController : ControllerBase
{
    private readonly ILogger<InstructionsController> logger;
    private readonly List<InstructionModel> instructions =
    [
        new("Coding", "Get assistance with code generation and debugging"),
        new("Documentation", "Generate clear and concise documentation"),
        new("Testing", "Help with test case creation and validation")
    ];

    public InstructionsController(ILogger<InstructionsController> logger)
    {
        this.logger = logger;
    }

    [HttpGet]
    public ActionResult<IEnumerable<InstructionModel>> GetAll()
    {
        logger.LogInformation("Retrieving all instructions");
        return Ok(instructions);
    }

    [HttpGet("{name}")]
    public ActionResult<InstructionModel> GetByName(string name)
    {
        var instruction = instructions.FirstOrDefault(i => i.Name == name);
        if (instruction == null)
        {
            logger.LogWarning("Instruction not found: {Name}", name);
            return NotFound();
        }

        logger.LogInformation("Retrieved instruction: {Name}", name);
        return Ok(instruction);
    }
}
