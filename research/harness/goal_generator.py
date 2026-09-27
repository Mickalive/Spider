"""
Goal Generator for EXP-GRAPH-36287167610
Deterministic goal generation with explicit train/validation/test splits
"""
import json
import hashlib
import random
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Goal:
    goal_id: str
    text: str
    target_mechanism_id: str
    category: str  # verbatim, paraphrased, underspecified, composite, no_applicable, ood_paraphrase
    applicable: bool  # True if at least one mechanism applies
    required_parameters: List[str]  # Parameters that should be bound
    family: str  # Resource family: users, posts, comments, albums, photos
    verb: str  # CREATE, READ, UPDATE, DELETE

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Distillation intents (verbatim goals source)
INTENTS = {
    "mech_users_create": "create a new user",
    "mech_users_read": "retrieve a user by id",
    "mech_users_update": "update a user",
    "mech_users_delete": "delete a user",
    "mech_posts_create": "create a new post",
    "mech_posts_read": "retrieve a post by id",
    "mech_posts_update": "update a post",
    "mech_posts_delete": "delete a post",
    "mech_comments_create": "create a new comment",
    "mech_comments_read": "retrieve a comment by id",
    "mech_comments_update": "update a comment",
    "mech_comments_delete": "delete a comment",
    "mech_albums_create": "create a new album",
    "mech_albums_read": "retrieve an album by id",
    "mech_albums_update": "update an album",
    "mech_albums_delete": "delete an album",
    "mech_photos_create": "create a new photo",
    "mech_photos_read": "retrieve a photo by id",
    "mech_photos_update": "update a photo",
    "mech_photos_delete": "delete a photo",
}

# Parameter slots per mechanism
PARAM_SLOTS = {
    "mech_users_create": ["user_id", "name", "email"],
    "mech_users_read": ["user_id"],
    "mech_users_update": ["user_id", "name", "email"],
    "mech_users_delete": ["user_id"],
    "mech_posts_create": ["post_id", "title", "body", "user_id"],
    "mech_posts_read": ["post_id"],
    "mech_posts_update": ["post_id", "title", "body"],
    "mech_posts_delete": ["post_id"],
    "mech_comments_create": ["comment_id", "post_id", "user_id", "body"],
    "mech_comments_read": ["comment_id"],
    "mech_comments_update": ["comment_id", "body"],
    "mech_comments_delete": ["comment_id"],
    "mech_albums_create": ["album_id", "title", "user_id"],
    "mech_albums_read": ["album_id"],
    "mech_albums_update": ["album_id", "title"],
    "mech_albums_delete": ["album_id"],
    "mech_photos_create": ["photo_id", "album_id", "title", "url"],
    "mech_photos_read": ["photo_id"],
    "mech_photos_update": ["photo_id", "title", "url"],
    "mech_photos_delete": ["photo_id"],
}

# Paraphrases for each intent (unseen wording)
PARAPHRASES = {
    "mech_users_create": [
        "add a new user to the system",
        "register a fresh user account",
        "make a new user profile",
    ],
    "mech_users_read": [
        "get a user by their id",
        "look up a user using id",
        "fetch user details by id",
    ],
    "mech_users_update": [
        "modify an existing user",
        "change user information",
        "edit a user's details",
    ],
    "mech_users_delete": [
        "remove a user from the system",
        "delete a user account",
        "erase a user profile",
    ],
    "mech_posts_create": [
        "write a new post",
        "publish a fresh post",
        "add a new blog post",
    ],
    "mech_posts_read": [
        "get a post by its id",
        "retrieve a post using id",
        "fetch post content by id",
    ],
    "mech_posts_update": [
        "edit an existing post",
        "modify a post's content",
        "change a post's title and body",
    ],
    "mech_posts_delete": [
        "remove a post",
        "delete a blog post",
        "take down a post",
    ],
    "mech_comments_create": [
        "add a new comment",
        "post a comment on a post",
        "write a comment",
    ],
    "mech_comments_read": [
        "get a comment by id",
        "fetch a comment using its id",
        "retrieve comment details",
    ],
    "mech_comments_update": [
        "edit a comment",
        "modify comment text",
        "change a comment's body",
    ],
    "mech_comments_delete": [
        "remove a comment",
        "delete a comment",
        "erase a comment",
    ],
    "mech_albums_create": [
        "create a new album",
        "make a fresh album",
        "add a new photo album",
    ],
    "mech_albums_read": [
        "get an album by id",
        "retrieve an album using id",
        "fetch album details",
    ],
    "mech_albums_update": [
        "edit an album",
        "modify album title",
        "change an album's name",
    ],
    "mech_albums_delete": [
        "remove an album",
        "delete a photo album",
        "erase an album",
    ],
    "mech_photos_create": [
        "add a new photo",
        "upload a photo to an album",
        "create a new photo entry",
    ],
    "mech_photos_read": [
        "get a photo by id",
        "fetch a photo using id",
        "retrieve photo details",
    ],
    "mech_photos_update": [
        "edit a photo",
        "modify photo title or url",
        "change a photo's metadata",
    ],
    "mech_photos_delete": [
        "remove a photo",
        "delete a photo from album",
        "erase a photo",
    ],
}

# Composite goals (combining multiple operations)
COMPOSITE_TEMPLATES = [
    ("create a {resource1} and then read it", "CREATE_READ"),
    ("create a {resource1}, update it, then delete it", "CREATE_UPDATE_DELETE"),
    ("read a {resource1} and create a related {resource2}", "READ_CREATE"),
    ("update a {resource1} then read it", "UPDATE_READ"),
]

# No-applicable goals (targeting operations/families not in registry)
NO_APPLICABLE_TEMPLATES = [
    "search for users by email",
    "list all posts by a user",
    "get comments for a post",
    "list photos in an album",
    "count users in the system",
    "find posts containing a keyword",
    "get recent activity feed",
    "export user data",
    "import users from csv",
    "backup the database",
    "login as a user",
    "logout current session",
    "change user password",
    "verify email address",
    "send notification to user",
    "create a tag for a post",
    "add a like to a post",
    "follow a user",
    "block a user",
    "generate report",
]

# OOD paraphrases (paraphrases of non-registry operations)
OOD_PARAPHRASES = [
    "find users by their email address",
    "show all posts written by a specific user",
    "retrieve comments belonging to a post",
    "list all photos inside an album",
    "count how many users exist",
    "search posts for a specific keyword",
    "get the latest activity feed",
    "export all user data to a file",
]


class GoalGenerator:
    def __init__(self, seed: int = 36287167610):
        self.seed = seed % (2**32)
        self.rng = random.Random(self.seed)
        self.split_seed = 990017

    def generate_all_goals(self) -> List[Goal]:
        """Generate all 80 goals with categories and labels"""
        goals = []
        goal_id = 0

        # 1. Verbatim goals (12) - exact copies of distillation intents
        verbatim_mechs = self.rng.sample(list(INTENTS.keys()), 12)
        for mech_id in verbatim_mechs:
            goal_id += 1
            family = mech_id.split("_")[1]
            verb = mech_id.split("_")[2].upper()
            goals.append(Goal(
                goal_id=f"goal_{goal_id:03d}",
                text=INTENTS[mech_id],
                target_mechanism_id=mech_id,
                category="verbatim",
                applicable=True,
                required_parameters=PARAM_SLOTS[mech_id].copy(),
                family=family,
                verb=verb
            ))

        # 2. Paraphrased goals (20) - unseen wording
        all_paraphrases = []
        for mech_id, paras in PARAPHRASES.items():
            for para in paras:
                all_paraphrases.append((mech_id, para))
        self.rng.shuffle(all_paraphrases)
        for mech_id, para in all_paraphrases[:20]:
            goal_id += 1
            family = mech_id.split("_")[1]
            verb = mech_id.split("_")[2].upper()
            goals.append(Goal(
                goal_id=f"goal_{goal_id:03d}",
                text=para,
                target_mechanism_id=mech_id,
                category="paraphrased",
                applicable=True,
                required_parameters=PARAM_SLOTS[mech_id].copy(),
                family=family,
                verb=verb
            ))

        # 3. Underspecified goals (10) - missing required parameters
        underspecified_mechs = self.rng.sample(list(INTENTS.keys()), 10)
        for mech_id in underspecified_mechs:
            goal_id += 1
            family = mech_id.split("_")[1]
            verb = mech_id.split("_")[2].upper()
            # Create a goal that mentions the operation but omits required params
            base_intent = INTENTS[mech_id]
            # Remove parameter-specific words to make it underspecified
            underspecified_text = self._make_underspecified(base_intent, mech_id)
            goals.append(Goal(
                goal_id=f"goal_{goal_id:03d}",
                text=underspecified_text,
                target_mechanism_id=mech_id,
                category="underspecified",
                applicable=True,  # A mechanism exists but params are missing
                required_parameters=PARAM_SLOTS[mech_id].copy(),
                family=family,
                verb=verb
            ))

        # 4. Composite goals (10) - combining multiple operations
        for i in range(10):
            goal_id += 1
            template, ctype = self.rng.choice(COMPOSITE_TEMPLATES)
            # Pick random resource families
            families = self.rng.sample(["users", "posts", "comments", "albums", "photos"], 2)
            text = template.format(resource1=families[0], resource2=families[1])
            # For composite, target the first operation's mechanism
            first_verb = ctype.split("_")[0].upper()
            target_mech = f"mech_{families[0]}_{first_verb.lower()}"
            family = families[0]
            verb = first_verb
            goals.append(Goal(
                goal_id=f"goal_{goal_id:03d}",
                text=text,
                target_mechanism_id=target_mech,
                category="composite",
                applicable=True,
                required_parameters=PARAM_SLOTS[target_mech].copy(),
                family=family,
                verb=verb
            ))

        # 5. No-applicable goals (20) - no mechanism in registry applies
        self.rng.shuffle(NO_APPLICABLE_TEMPLATES)
        for text in NO_APPLICABLE_TEMPLATES[:20]:
            goal_id += 1
            goals.append(Goal(
                goal_id=f"goal_{goal_id:03d}",
                text=text,
                target_mechanism_id="",  # No applicable mechanism
                category="no_applicable",
                applicable=False,
                required_parameters=[],
                family="",
                verb=""
            ))

        # 6. OOD paraphrase goals (8) - paraphrases of non-registry operations
        self.rng.shuffle(OOD_PARAPHRASES)
        for text in OOD_PARAPHRASES[:8]:
            goal_id += 1
            goals.append(Goal(
                goal_id=f"goal_{goal_id:03d}",
                text=text,
                target_mechanism_id="",
                category="ood_paraphrase",
                applicable=False,
                required_parameters=[],
                family="",
                verb=""
            ))

        assert len(goals) == 80, f"Expected 80 goals, got {len(goals)}"
        return goals

    def _make_underspecified(self, intent: str, mech_id: str) -> str:
        """Create an underspecified version by removing parameter references"""
        # Simple transformation: remove specific parameter mentions
        underspecified = intent
        slots = PARAM_SLOTS[mech_id]
        for slot in slots:
            # Remove patterns like "by id", "with id", etc.
            underspecified = underspecified.replace(f"by {slot}", "").replace(f"with {slot}", "").replace(slot, "")
        underspecified = " ".join(underspecified.split()).strip()
        if not underspecified or len(underspecified) < 5:
            underspecified = f"do something with {mech_id.split('_')[1]}"
        return underspecified

    def split_goals(self, goals: List[Goal]) -> Tuple[List[Goal], List[Goal], List[Goal]]:
        """Split goals into train/validation/test by resource family (stratified)"""
        # Separate applicable and no-applicable
        applicable = [g for g in goals if g.applicable]
        no_applicable = [g for g in goals if not g.applicable]

        # Stratified split by family for applicable goals
        train_app, val_app, test_app = self._stratified_split(applicable, 0.6, 0.2, 0.2)
        # Split no-applicable
        train_na, val_na, test_na = self._stratified_split(no_applicable, 0.6, 0.2, 0.2)

        train = train_app + train_na
        validation = val_app + val_na
        test = test_app + test_na

        self.rng.shuffle(train)
        self.rng.shuffle(validation)
        self.rng.shuffle(test)

        return train, validation, test

    def _stratified_split(self, goals: List[Goal], train_frac: float, val_frac: float, test_frac: float) -> Tuple[List[Goal], List[Goal], List[Goal]]:
        """Stratified split by family"""
        by_family = {}
        for g in goals:
            fam = g.family if g.family else "no_applicable"
            if fam not in by_family:
                by_family[fam] = []
            by_family[fam].append(g)

        train, val, test = [], [], []
        for fam, fam_goals in by_family.items():
            self.rng.shuffle(fam_goals)
            n = len(fam_goals)
            n_train = max(1, int(n * train_frac))
            n_val = max(1, int(n * val_frac))
            n_test = n - n_train - n_val
            if n_test < 1 and n > n_train + n_val:
                n_test = 1
                n_val = n - n_train - n_test

            train.extend(fam_goals[:n_train])
            val.extend(fam_goals[n_train:n_train + n_val])
            test.extend(fam_goals[n_train + n_val:])

        return train, val, test


def save_goals(goals: List[Goal], path: str):
    """Save goals to JSON file"""
    data = [g.to_dict() for g in goals]
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def load_goals(path: str) -> List[Goal]:
    """Load goals from JSON file"""
    with open(path, 'r') as f:
        data = json.load(f)
    return [Goal(**d) for d in data]


def compute_goals_hash(goals: List[Goal]) -> str:
    """Compute SHA256 of goals list"""
    serialized = json.dumps([g.to_dict() for g in goals], sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


if __name__ == "__main__":
    gen = GoalGenerator()
    goals = gen.generate_all_goals()

    # Print category counts
    from collections import Counter
    cat_counts = Counter(g.category for g in goals)
    print("Category counts:")
    for cat, count in cat_counts.items():
        print(f"  {cat}: {count}")

    app_count = sum(1 for g in goals if g.applicable)
    na_count = sum(1 for g in goals if not g.applicable)
    print(f"\nApplicable: {app_count}")
    print(f"No-applicable: {na_count}")

    # Split
    train, val, test = gen.split_goals(goals)
    print(f"\nTrain: {len(train)} (applicable: {sum(1 for g in train if g.applicable)}, no-applicable: {sum(1 for g in train if not g.applicable)})")
    print(f"Val: {len(validation)} (applicable: {sum(1 for g in validation if g.applicable)}, no-applicable: {sum(1 for g in validation if not g.applicable)})")
    print(f"Test: {len(test)} (applicable: {sum(1 for g in test if g.applicable)}, no-applicable: {sum(1 for g in test if not g.applicable)})")

    # Save
    save_goals(goals, "goals.json")
    print("\nGoals saved to goals.json")
    print(f"Goals hash: {compute_goals_hash(goals)}")