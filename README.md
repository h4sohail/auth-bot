# Authentication Bot

An authentication bot that verifies Discord users using the university email address of students

When a user joins, they are promted to enter their student ID, bot then finds the email of the student using the student ID and emails them a unique code, when the user enters the code they get access to the Discord server.

For security reasons the actual process of getting university emails from a student ID is not part of this public repository, but it can be easily added in, or read in with a "students.json", where, "students.json" is structured as such:   

```json
{
   "101160":{
      "First Name": "John",
      "Last Name": "Doe",
      "Email": "john@uni.com"
   },
   "101149":{
      "First Name": "Doe",
      "Last Name": "John",
      "Email": "doe@uni.com"
  }
}
```
