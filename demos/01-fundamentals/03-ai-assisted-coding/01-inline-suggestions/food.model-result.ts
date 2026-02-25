// create a class that represents the data structure of the food (name, price, description, calories) for a restaurant, use the constructor to initialize the properties of the class

export class Food {
  name: string;
  price: number;
  description: string;
  calories: number;

  constructor(name: string, price: number, description: string, calories: number) {
    this.name = name;
    this.price = price;
    this.description = description;
    this.calories = calories;
  }
}
