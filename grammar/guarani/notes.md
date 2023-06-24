Considerations:
We cannot have more symbols in right hand side than left hand side, due to how syntactic transfer works.
We cannot have both symbols and terminals in the right hand side of a rule.
We cannot have the same symbol twice on the right hand side of a rule. This is due to how syntactic transfer works, which needs to know how variables are ordered. We can use auxiliary variables to address that issue.
We cannot have the same name for different features that we mean to unify (kinda obvious tbh).
We cannot try to unify on nested features, only top level features.
We cannot use the same variable on different features (kinda obvious tbh too).