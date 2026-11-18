# Adding features

Style is the initial preference feature. A future feature such as register or terminology should define its allowed values, instructions, candidate guidance, validation criteria, and preference-record construction. Keep feature-specific rules with the stage that uses them. Put rules reused by multiple stages in shared code so training can operate on the same preference-record interface.

The feature interface and prompt formatter are deferred.
