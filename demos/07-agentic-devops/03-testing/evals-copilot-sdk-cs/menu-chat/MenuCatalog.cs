using System.Text;

namespace MenuChat;

public sealed record MenuItem(string Name, decimal PriceEur, int Stock, bool Vegetarian, string Description);

public static class MenuCatalog
{
    public static readonly IReadOnlyList<MenuItem> Items =
    [
        new MenuItem(
            "Hand pulled Noodles",
            17m,
            9,
            false,
            "Hand pulled noodles made with love by our experienced cooks from Sichuan. Served with your choice of meat, vegetables, and smashed cucumber salad."),
        new MenuItem(
            "Pad Kra Pao",
            16m,
            12,
            false,
            "Pad Kra Pao definitely one of the most popular spicy dishes in Thailand. Cooked with thai holy basil, long beans and chicken. Served with jasmine rice and fried egg."),
        new MenuItem(
            "Wiener Schnitzel",
            18m,
            13,
            false,
            "Wiener Schnitzel is a traditional Austrian dish consisting of a thin slice of veal coated in breadcrumbs and fried. Served with potato salad and lemon."),
        new MenuItem(
            "Falafel Plate",
            12m,
            9,
            true,
            "Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad."),
        new MenuItem(
            "Pizza Tartufo",
            24m,
            4,
            true,
            "Pizza truffle is well tasting, exclusive joy for your taste bud. A delight of white pizza where the protagonist is our cheese with truffle flakes.")
    ];

    public static string BuildSystemPrompt()
    {
        StringBuilder builder = new();
        builder.AppendLine("You are the menu assistant for a small food shop.");
        builder.AppendLine("Rules:");
        builder.AppendLine("- Answer only from the menu items listed below. Never invent a dish that is not listed.");
        builder.AppendLine("- If the customer asks about a dish that is not on the menu, say clearly that it is not on the menu.");
        builder.AppendLine("- Always give prices in EUR.");
        builder.AppendLine("- Keep answers short, at most two sentences.");
        builder.AppendLine();
        builder.AppendLine("Menu:");
        foreach (MenuItem item in Items)
        {
            builder.AppendLine($"- {FormatItem(item)}");
        }

        return builder.ToString();
    }

    public static string FormatItem(MenuItem item) =>
        $"{item.Name}: {item.PriceEur} EUR, {item.Stock} in stock, {(item.Vegetarian ? "vegetarian" : "not vegetarian")}. {item.Description}";
}
