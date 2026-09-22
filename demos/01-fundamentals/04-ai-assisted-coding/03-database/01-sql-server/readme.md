# Prompting for SQL

Execute these prompts with [SQL Server - VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql)

Step 1: Create a Food table

```sql
create a table for microsoft sql server azure to store the data of the following type:

export type Food = {
    name: string;
    price: number;
    description: string;
    category: string;
};
```

Step 2: Create a view for budget items

```sql
create a view to get the food items with price less than 10
```

Step 3: Create a stored procedure to filter by category

```sql
create a stored procedure to get all the food items in a certain category
```

Step 4: Create a stored procedure to insert items

```sql
create a stored procedure to insert a new food item
```

Step 5: Generate sample data

```sql
generate some sample data to insert into the table using the stored procedure
```
