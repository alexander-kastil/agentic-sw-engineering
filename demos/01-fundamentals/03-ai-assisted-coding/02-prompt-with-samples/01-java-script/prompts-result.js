const users = [
  { name: 'John Doe', age: 30, city: 'New York' },
  { name: 'Jane Fonda', age: 25, city: 'Los Angeles' },
  { name: 'Jim the cat', age: 40, city: 'Chicago' }
];

function filterUserByName(name) {
  return users.find(user => user.name === name);
}

console.log(filterUserByName('Jane Fonda'));

