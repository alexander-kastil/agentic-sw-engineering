# JavaScript - Prompt with Samples

Learn how providing code samples helps Copilot understand your intent and generate precise implementations. Each example shows a prompt paired with expected code output.

## Example: Object Creation with Sample Data

```prompt
create an array of users:
name: 'John Doe', age: 30, city: 'New York'
name: 'Jane Fonda', age: 25, city: 'Los Angeles'
name: 'Jim the cat', age: 40, city: 'Chicago'
```

Generated Code:

```
const users = [
  { name: 'John Doe', age: 30, city: 'New York' },
  { name: 'Jane Fonda', age: 25, city: 'Los Angeles' },
  { name: 'Jim the cat', age: 40, city: 'Chicago' }
];
```

Prompt:

```prompt
Create a function to filter on of the users by name
```

Generated Code:

function filterUserByName(name) {
  return users.find(user => user.name === name);
}
```

```prompt
Call the function with 'Jane Fonda' and log it to the console
```

