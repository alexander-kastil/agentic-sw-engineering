package catalog

type Item struct {
	ID          int     `json:"id"`
	Name        string  `json:"name"`
	Price       float64 `json:"price"`
	InStock     int     `json:"inStock"`
	PictureURL  *string `json:"pictureUrl"`
	Description *string `json:"description"`
}

func text(value string) *string {
	return &value
}

var seedItems = []Item{
	{
		ID:          1,
		Name:        "Hand pulled Noodles",
		InStock:     9,
		Price:       17,
		PictureURL:  text("hand-pulled-noodles.png"),
		Description: text("Hand pulled noodles made with love by our experienced cooks from Sichuan. Served with your choice of meat, vegetables, and smashed cucumber salad."),
	},
	{
		ID:          2,
		Name:        "Pad Kra Pao",
		InStock:     12,
		Price:       16,
		PictureURL:  text("pad-kra-pao.png"),
		Description: text("Pad Kra Pao definitely one of the most popular spicy dishes in Thailand. Cooked with thai holy basil, long beans and chicken. Served with jasmine rice and fried egg."),
	},
	{
		ID:          3,
		Name:        "Wiener Schnitzel",
		InStock:     13,
		Price:       18,
		PictureURL:  text("schnitzel.jpg"),
		Description: text("Wiener Schnitzel is a traditional Austrian dish consisting of a thin slice of veal coated in breadcrumbs and fried. Served with potato salad and lemon."),
	},
	{
		ID:          4,
		Name:        "Falafel Plate",
		InStock:     9,
		Price:       12,
		PictureURL:  text("falafel.jpg"),
		Description: text("Falafel is a deep-fried ball, doughnut or patty made from ground chickpeas. Served with hummus, pita bread, and salad."),
	},
	{
		ID:          5,
		Name:        "Pizza Tartufo",
		InStock:     4,
		Price:       24,
		PictureURL:  text("pizza.jpg"),
		Description: text("Pizza truffle is well tasting, exclusive joy for your taste bud. A delight of white pizza where the protagonist is our cheese with truffle flakes."),
	},
}
