# WORKFLOW

## Key Conventions
- **scenes** = UI page/screen
- **docs/workflow** = project documentation
- **scripts/seed** = data seeding
- **scripts/deploy** = deployment configs
- **infra/** = infrastructure-as-code

## Value Prop
A student registers once, speaks or types their profile in their language.
The AI matches them to all eligible scholarships, shows a checklist,
and pings them before deadlines — all in one place.

## Development Lifecycle
Discovery/Research     ->   1, 2
Design/Prototyping     ->   3, 4
Backend Development    ->   4, 5, 6, 7
Frontend Development   ->   6, 8
Integration/Automation ->   7, 9
Testing                ->   8, 9, 10
Deployment             ->   9, 10
Iteration              ->  10

## Repo Map
backend     -> 3, 4, 5, 6, 9
frontend    -> 3, 6, 10
data        -> 1, 2, 3, 4
ai-ml       -> 4, 5, 6
infra       -> 7, 9, 10
docs        -> 1, 2, 3, 4
scripts     -> 7, 10
