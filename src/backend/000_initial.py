import os
import json
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if hasattr(main, 'seed_sample'):
    main.seed_sample()
print("Database seeded")
