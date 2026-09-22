using System.Collections.Generic;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FoodApp
{
    [Route("[controller]")]
    [ApiController]
    public class CatsController(FoodDBContext ctx) : ControllerBase
    {
        // http://localhost:PORT/cats
        [HttpGet()]
        public async Task<IEnumerable<Cat>> GetCats()
        {
            return await ctx.Cats.ToArrayAsync();
        }

        // http://localhost:PORT/cats/3
        [HttpGet("{id}")]
        public async Task<Cat> GetById(int id)
        {
            return await ctx.Cats.FirstOrDefaultAsync(c => c.ID == id);
        }

        // http://localhost:PORT/cats
        [HttpPost()]
        public async Task<Cat> CreateCat(Cat cat)
        {
            ctx.Cats.Add(cat);
            await ctx.SaveChangesAsync();
            return cat;
        }

        // http://localhost:PORT/cats
        [HttpPut()]
        public async Task<Cat> UpdateCat(Cat cat)
        {
            ctx.Cats.Attach(cat);
            ctx.Entry(cat).State = EntityState.Modified;
            await ctx.SaveChangesAsync();
            return cat;
        }

        // http://localhost:PORT/cats/3
        [HttpDelete("{id}")]
        public async Task<ActionResult> DeleteCat(int id)
        {
            var cat = await GetById(id);
            if (cat != null)
            {
                ctx.Remove(cat);
                await ctx.SaveChangesAsync();
            }
            return Ok();
        }
    }
}
