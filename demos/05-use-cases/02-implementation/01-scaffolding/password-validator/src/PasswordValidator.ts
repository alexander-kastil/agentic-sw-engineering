export class PasswordValidator {
  validate(password: string): boolean {
    return password.length >= 6;
  }
}