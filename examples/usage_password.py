from allsafe_auth.security.password_manager import PasswordManager, PasswordPolicy

# No restriction (any password is allowed)
pm_none = PasswordManager(policy=PasswordPolicy.no_restriction())

# Medium restriction (min 8, must have digit + lowercase)
pm_medium = PasswordManager(policy=PasswordPolicy.medium())

# Strong restriction (min 12, must have digit, upper, lower, special)
pm_strong = PasswordManager(policy=PasswordPolicy.strong())

print(pm_none.validate_password_strength("123"))               # ✅ True
print(pm_medium.validate_password_strength("abc123"))          # ❌ False (too short)
print(pm_medium.validate_password_strength("abc12345"))        # ✅ True
print(pm_strong.validate_password_strength("Abc123!@#def"))    # ✅ True
print(pm_strong.validate_password_strength("123456789012"))    # ❌ False (missing upper/lower/special)
