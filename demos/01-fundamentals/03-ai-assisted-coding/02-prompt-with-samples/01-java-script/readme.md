# JavaScript - Prompt with Samples

Learn how providing code samples helps Copilot understand your intent and generate precise implementations. Each example shows a prompt paired with expected code output.

## Example 1: API Data Retrieval

Prompt:

```prompt
// Pass in user ids and retrieve user data from jsonplaceholder.typicode.com API, then return it as a JSON object
```

Generated Code:

```javascript
async function getUserData(userId) {
    const response = await fetch(`https://jsonplaceholder.typicode.com/users/${userId}`);
    const data = await response.json();
    return data;
}
```

## Example 2: Array Flattening and Mapping

Prompt:

```prompt
Map through an array of arrays of objects
Example: Extract names from the data array
Desired outcome: ['John', 'Jane', 'Bob']
```

Generated Code:

```javascript
const data = [
[{ name: 'John', age: 25 }, { name: 'Jane', age: 30 }],
[{ name: 'Bob', age: 40 }]
];
const mappedData = data.flatMap(sublist => sublist.map(person => person.name));
console.log(mappedData);
```
