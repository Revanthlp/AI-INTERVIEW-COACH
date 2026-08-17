import json
import re
from pathlib import Path
from transformers import pipeline


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("Loading AI model...")

generator = pipeline(
    "text-generation",
    model=MODEL_NAME
)

print("AI model loaded successfully!")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = (
    BASE_DIR / "data" / "questions.json"
)


# ============================================================
# AI GENERATION
# ============================================================

def _generate(messages, max_new_tokens=150):

    result = generator(
        messages,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=0.1,
        top_p=0.9,
        clean_up_tokenization_spaces=False,
    )

    generated_text = result[0]["generated_text"]

    if isinstance(generated_text, list):
        return generated_text[-1]["content"].strip()

    return generated_text.strip()


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def _normalize_text(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    replacements = {
        "key-value": "key value",
        "key/value": "key value",
        "high-level": "high level",
        "object-oriented": "object oriented",
        "retrieval-augmented": "retrieval augmented",
        "large-language-model": "large language model",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(
        r"[^a-z0-9+#.\- ]+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def _words(text):

    return set(
        word
        for word in _normalize_text(text).split()
        if len(word) > 2
    )


# ============================================================
# LOAD QUESTION BANK
# ============================================================

def _load_questions():

    if not QUESTIONS_FILE.exists():
        return []

    try:

        with open(
            QUESTIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

    except Exception:
        pass

    return []


def _get_question_metadata(question):

    questions = _load_questions()

    normalized_question = _normalize_text(
        question
    )

    for item in questions:

        if not isinstance(item, dict):
            continue

        stored_question = _normalize_text(
            item.get("question", "")
        )

        if stored_question == normalized_question:
            return item

    return {}


# ============================================================
# QUESTION CONCEPT DATABASE
# ============================================================

QUESTION_CONCEPTS = {

    "what is python": [
        {
            "name": "python",
            "aliases": [
                "python"
            ]
        },
        {
            "name": "programming language",
            "aliases": [
                "programming language"
            ]
        },
        {
            "name": "high level",
            "aliases": [
                "high level",
                "general purpose"
            ]
        },
        {
            "name": "common uses",
            "aliases": [
                "web development",
                "data analysis",
                "automation",
                "machine learning"
            ]
        }
    ],

    "what are python dictionaries": [
        {
            "name": "dictionary",
            "aliases": [
                "dictionary",
                "dictionaries"
            ]
        },
        {
            "name": "key value pairs",
            "aliases": [
                "key value",
                "key value pair",
                "key value pairs"
            ]
        },
        {
            "name": "keys",
            "aliases": [
                "key",
                "keys"
            ]
        },
        {
            "name": "values",
            "aliases": [
                "value",
                "values"
            ]
        },
        {
            "name": "mutable",
            "aliases": [
                "mutable",
                "mutability"
            ]
        },
        {
            "name": "unique keys",
            "aliases": [
                "unique keys",
                "keys are unique",
                "each key is unique",
                "every key is unique"
            ]
        }
    ],

    "what is oop in python": [
        {
            "name": "object oriented programming",
            "aliases": [
                "object oriented programming",
                "oop"
            ]
        },
        {
            "name": "classes",
            "aliases": [
                "class",
                "classes"
            ]
        },
        {
            "name": "objects",
            "aliases": [
                "object",
                "objects"
            ]
        },
        {
            "name": "encapsulation",
            "aliases": [
                "encapsulation"
            ]
        },
        {
            "name": "inheritance",
            "aliases": [
                "inheritance"
            ]
        },
        {
            "name": "polymorphism",
            "aliases": [
                "polymorphism"
            ]
        }
    ],

    "what is the difference between a list and a tuple in python": [
        {
            "name": "list",
            "aliases": [
                "list",
                "lists"
            ]
        },
        {
            "name": "tuple",
            "aliases": [
                "tuple",
                "tuples"
            ]
        },
        {
            "name": "list mutable",
            "aliases": [
                "list is mutable",
                "lists are mutable",
                "mutable list",
                "lists can be changed"
            ]
        },
        {
            "name": "tuple immutable",
            "aliases": [
                "tuple is immutable",
                "tuples are immutable",
                "immutable tuple",
                "tuples cannot be changed"
            ]
        }
    ],

    "what is supervised learning": [
        {
            "name": "supervised learning",
            "aliases": [
                "supervised learning"
            ]
        },
        {
            "name": "labeled data",
            "aliases": [
                "labeled data",
                "labelled data"
            ]
        },
        {
            "name": "training data",
            "aliases": [
                "training data",
                "training set"
            ]
        },
        {
            "name": "input features",
            "aliases": [
                "input",
                "features"
            ]
        },
        {
            "name": "output target",
            "aliases": [
                "output",
                "target",
                "label"
            ]
        },
        {
            "name": "prediction",
            "aliases": [
                "prediction",
                "predictions"
            ]
        }
    ],

    "what is overfitting": [
        {
            "name": "overfitting",
            "aliases": [
                "overfitting"
            ]
        },
        {
            "name": "training data",
            "aliases": [
                "training data",
                "training set"
            ]
        },
        {
            "name": "unseen data",
            "aliases": [
                "unseen data",
                "test data",
                "testing data"
            ]
        },
        {
            "name": "generalization",
            "aliases": [
                "generalization",
                "generalise",
                "generalize"
            ]
        },
        {
            "name": "poor test performance",
            "aliases": [
                "poor test performance",
                "poor performance on unseen data"
            ]
        }
    ],

    "what is retrieval augmented generation rag": [
        {
            "name": "retrieval augmented generation",
            "aliases": [
                "retrieval augmented generation",
                "rag"
            ]
        },
        {
            "name": "retrieval",
            "aliases": [
                "retrieval",
                "retrieve",
                "retrieves"
            ]
        },
        {
            "name": "external knowledge",
            "aliases": [
                "documents",
                "external knowledge",
                "knowledge base"
            ]
        },
        {
            "name": "context",
            "aliases": [
                "context"
            ]
        },
        {
            "name": "large language model",
            "aliases": [
                "large language model",
                "llm"
            ]
        },
        {
            "name": "generation",
            "aliases": [
                "generation",
                "generate"
            ]
        }
    ],

    "what is an llm": [
        {
            "name": "large language model",
            "aliases": [
                "large language model",
                "llm"
            ]
        },
        {
            "name": "language model",
            "aliases": [
                "language model"
            ]
        },
        {
            "name": "text",
            "aliases": [
                "text"
            ]
        },
        {
            "name": "tokens",
            "aliases": [
                "token",
                "tokens"
            ]
        },
        {
            "name": "training",
            "aliases": [
                "training",
                "trained"
            ]
        }
    ],

    "what is sql": [
        {
            "name": "structured query language",
            "aliases": [
                "structured query language",
                "sql"
            ]
        },
        {
            "name": "database",
            "aliases": [
                "database",
                "databases"
            ]
        },
        {
            "name": "relational database",
            "aliases": [
                "relational database",
                "relational databases"
            ]
        },
        {
            "name": "query",
            "aliases": [
                "query",
                "queries"
            ]
        }
    ],

    "what is machine learning": [
        {
            "name": "machine learning",
            "aliases": [
                "machine learning"
            ]
        },
        {
            "name": "data",
            "aliases": [
                "data"
            ]
        },
        {
            "name": "patterns",
            "aliases": [
                "patterns",
                "patterns in data"
            ]
        },
        {
            "name": "prediction",
            "aliases": [
                "prediction",
                "predictions"
            ]
        }
    ],

    "what is deep learning": [
        {
            "name": "deep learning",
            "aliases": [
                "deep learning"
            ]
        },
        {
            "name": "neural networks",
            "aliases": [
                "neural network",
                "neural networks"
            ]
        },
        {
            "name": "multiple layers",
            "aliases": [
                "multiple layers",
                "layers"
            ]
        },
        {
            "name": "machine learning",
            "aliases": [
                "machine learning"
            ]
        }
    ]
}


# ============================================================
# EXPECTED CONCEPTS
# ============================================================

def _get_expected_concepts(question):

    metadata = _get_question_metadata(
        question
    )

    metadata_concepts = metadata.get(
        "expected_concepts",
        []
    )

    if isinstance(
        metadata_concepts,
        list
    ):

        concepts = []

        for item in metadata_concepts:

            if isinstance(item, str):

                concepts.append({
                    "name": item,
                    "aliases": [item]
                })

            elif isinstance(item, dict):

                concepts.append(item)

        if concepts:
            return concepts

    normalized_question = _normalize_text(
        question
    )

    for key, concepts in QUESTION_CONCEPTS.items():

        normalized_key = _normalize_text(
            key
        )

        if normalized_question == normalized_key:
            return concepts

    return []


# ============================================================
# NEGATION / CONTRADICTION HELPERS
# ============================================================

NEGATION_WORDS = {
    "not",
    "no",
    "never",
    "without",
    "cannot",
    "cant",
    "isnt",
    "isn't",
    "are not",
    "are'nt",
    "does not",
    "do not",
    "doesnt",
    "don't",
    "doesn't"
}


def _is_negated(
    text,
    phrase
):

    normalized_text = _normalize_text(
        text
    )

    normalized_phrase = _normalize_text(
        phrase
    )

    position = normalized_text.find(
        normalized_phrase
    )

    if position == -1:
        return False

    before = normalized_text[
        max(0, position - 45):
        position
    ]

    before_words = before.split()

    if not before_words:
        return False

    recent_words = before_words[-6:]

    for word in recent_words:

        if word in NEGATION_WORDS:
            return True

    # Specific negative constructions.
    negative_patterns = [
        f"without {normalized_phrase}",
        f"no {normalized_phrase}",
        f"not {normalized_phrase}",
        f"never {normalized_phrase}",
        f"does not {normalized_phrase}",
        f"do not {normalized_phrase}",
        f"cannot {normalized_phrase}",
    ]

    return any(
        pattern in normalized_text
        for pattern in negative_patterns
    )


def _contains_word(
    text,
    word
):

    normalized = _normalize_text(
        text
    )

    return word in normalized.split()


# ============================================================
# CONCEPT CONTRADICTIONS
# ============================================================

def _dictionary_contradictions(answer):

    normalized = _normalize_text(
        answer
    )

    contradictions = []

    # --------------------------------------------------------
    # Mutable / immutable
    # --------------------------------------------------------

    if (
        "immutable" in normalized
        and
        "mutable" not in normalized
    ):

        contradictions.append(
            "The answer incorrectly says dictionaries are immutable. Python dictionaries are mutable."
        )

    if (
        "immutable" in normalized
        and
        "mutable" in normalized
    ):

        # Check whether immutable is actually describing
        # something else.
        if re.search(
            r"dictionary.{0,60}immutable",
            normalized
        ):

            contradictions.append(
                "The answer incorrectly describes Python dictionaries as immutable."
            )

    # --------------------------------------------------------
    # Only values / without keys
    # --------------------------------------------------------

    negative_key_patterns = [
        "without keys",
        "without a key",
        "without key",
        "no keys",
        "no key",
        "only values",
        "values without keys"
    ]

    for pattern in negative_key_patterns:

        if pattern in normalized:

            contradictions.append(
                "The answer incorrectly says dictionaries do not use keys. Dictionaries store key-value pairs."
            )

            break

    # --------------------------------------------------------
    # Duplicate keys
    # --------------------------------------------------------

    duplicate_key_patterns = [
        "keys can duplicate",
        "keys can be duplicated",
        "duplicate keys are allowed",
        "duplicate keys are allowed"
    ]

    for pattern in duplicate_key_patterns:

        if pattern in normalized:

            contradictions.append(
                "The answer incorrectly says duplicate dictionary keys are allowed. Dictionary keys are unique."
            )

            break

    return contradictions


# ============================================================
# GENERIC CONTRADICTIONS
# ============================================================

def _find_contradictions(
    question,
    answer
):

    normalized_question = _normalize_text(
        question
    )

    contradictions = []

    if (
        "dictionary" in normalized_question
        or
        "dictionaries" in normalized_question
    ):

        contradictions.extend(
            _dictionary_contradictions(
                answer
            )
        )

    return list(
        dict.fromkeys(
            contradictions
        )
    )


# ============================================================
# CONCEPT MATCHING
# ============================================================

def _concept_present(
    answer,
    concept
):

    if isinstance(
        concept,
        str
    ):

        name = concept
        aliases = [concept]

    else:

        name = concept.get(
            "name",
            ""
        )

        aliases = concept.get(
            "aliases",
            [name]
        )

    normalized_answer = _normalize_text(
        answer
    )

    # --------------------------------------------------------
    # Special handling for dictionary concepts.
    # --------------------------------------------------------

    if name == "mutable":

        if (
            "immutable" in normalized_answer
            and
            "mutable" not in normalized_answer
        ):

            return False

        if _is_negated(
            normalized_answer,
            "mutable"
        ):

            return False

    if name == "unique keys":

        unique_patterns = [
            "unique keys",
            "keys are unique",
            "each key is unique",
            "every key is unique",
            "each key must be unique"
        ]

        for pattern in unique_patterns:

            if pattern in normalized_answer:

                return True

        return False

    if name == "key value pairs":

        positive_patterns = [
            "key value pair",
            "key value pairs",
            "key and value",
            "keys and values",
            "key is used to access",
            "keys are used to access"
        ]

        for pattern in positive_patterns:

            if pattern in normalized_answer:

                if not _is_negated(
                    normalized_answer,
                    pattern
                ):

                    return True

        return False

    if name == "keys":

        # "without keys" must NOT count.
        if (
            "without keys" in normalized_answer
            or
            "without a key" in normalized_answer
            or
            "without key" in normalized_answer
            or
            "no keys" in normalized_answer
            or
            "no key" in normalized_answer
        ):

            return False

        key_patterns = [
            "keys",
            "key",
            "each key",
            "every key"
        ]

        for pattern in key_patterns:

            if pattern in normalized_answer:

                if not _is_negated(
                    normalized_answer,
                    pattern
                ):

                    return True

        return False

    if name == "values":

        value_patterns = [
            "values",
            "value",
            "corresponding value",
            "corresponding values",
            "key value",
            "key value pair",
            "key value pairs"
        ]

        for pattern in value_patterns:

            if pattern in normalized_answer:

                if not _is_negated(
                    normalized_answer,
                    pattern
                ):

                    return True

        return False

    # --------------------------------------------------------
    # Normal concept matching.
    # --------------------------------------------------------

    for alias in aliases:

        normalized_alias = _normalize_text(
            alias
        )

        if not normalized_alias:
            continue

        if normalized_alias in normalized_answer:

            if not _is_negated(
                normalized_answer,
                normalized_alias
            ):

                return True

    return False


def _calculate_concept_coverage(
    answer,
    concepts
):

    if not concepts:

        return {
            "coverage": None,
            "matched": [],
            "missing": []
        }

    matched = []
    missing = []

    for concept in concepts:

        name = (
            concept
            if isinstance(
                concept,
                str
            )
            else concept.get(
                "name",
                ""
            )
        )

        if _concept_present(
            answer,
            concept
        ):

            matched.append(
                name
            )

        else:

            missing.append(
                name
            )

    coverage = (
        len(matched)
        /
        len(concepts)
    )

    return {
        "coverage": coverage,
        "matched": matched,
        "missing": missing
    }


# ============================================================
# BASIC ANSWER CHECKS
# ============================================================

def _is_empty_answer(answer):

    return not answer.strip()


def _is_dont_know_answer(answer):

    normalized = _normalize_text(
        answer
    )

    patterns = [
        "i dont know",
        "i do not know",
        "dont know",
        "do not know",
        "no idea",
        "not sure",
        "i have no idea",
        "cannot answer",
        "cant answer"
    ]

    return any(
        pattern in normalized
        for pattern in patterns
    )


def _is_too_short(answer):

    return len(
        _words(answer)
    ) < 4


# ============================================================
# DETERMINISTIC SCORING
# ============================================================

def _deterministic_evaluation(
    question,
    answer
):

    answer = answer.strip()

    if _is_empty_answer(answer):

        return {
            "overall_score": 0,
            "correctness": 0,
            "relevance": 0,
            "clarity": 0,
            "completeness": 0,
            "strengths": [],
            "improvements": [
                "Provide an actual answer to the interview question."
            ],
            "better_answer": ""
        }

    if _is_dont_know_answer(answer):

        return {
            "overall_score": 1,
            "correctness": 0,
            "relevance": 1,
            "clarity": 2,
            "completeness": 0,
            "strengths": [],
            "improvements": [
                "You did not provide a substantive answer.",
                "Explain the basic concept in your own words."
            ],
            "better_answer": ""
        }

    concepts = _get_expected_concepts(
        question
    )

    coverage = _calculate_concept_coverage(
        answer,
        concepts
    )

    contradictions = _find_contradictions(
        question,
        answer
    )

    # --------------------------------------------------------
    # Known question.
    # --------------------------------------------------------

    if coverage["coverage"] is not None:

        ratio = coverage["coverage"]

        # ----------------------------------------------------
        # First handle factual contradictions.
        # ----------------------------------------------------

        if contradictions:

            correctness = 1
            relevance = 3
            completeness = 2

            overall = 2

            strengths = []

            improvements = (
                contradictions.copy()
            )

            if coverage["missing"]:

                improvements.append(
                    "Also explain: "
                    + ", ".join(
                        coverage["missing"][:5]
                    )
                    + "."
                )

            return {
                "overall_score": overall,
                "correctness": correctness,
                "relevance": relevance,
                "clarity": 5,
                "completeness": completeness,
                "strengths": strengths,
                "improvements": improvements,
                "better_answer": ""
            }

        # ----------------------------------------------------
        # Normal scoring.
        # ----------------------------------------------------

        if ratio == 0:

            correctness = 1
            relevance = 1
            completeness = 1

        elif ratio < 0.25:

            correctness = 3
            relevance = 3
            completeness = 2

        elif ratio < 0.50:

            correctness = 5
            relevance = 6
            completeness = 4

        elif ratio < 0.75:

            correctness = 7
            relevance = 8
            completeness = 6

        elif ratio < 1.0:

            correctness = 8
            relevance = 9
            completeness = 8

        else:

            correctness = 9
            relevance = 9
            completeness = 9

        # Very short answers cannot be perfect.
        if _is_too_short(answer):

            correctness = min(
                correctness,
                5
            )

            completeness = min(
                completeness,
                4
            )

        # ----------------------------------------------------
        # Clarity.
        # ----------------------------------------------------

        word_count = len(
            _words(answer)
        )

        if word_count < 5:

            clarity = 5

        elif word_count < 10:

            clarity = 7

        elif word_count < 60:

            clarity = 9

        else:

            clarity = 8

        # ----------------------------------------------------
        # Overall score.
        # ----------------------------------------------------

        overall = round(
            (
                correctness * 0.40
                +
                relevance * 0.20
                +
                clarity * 0.10
                +
                completeness * 0.30
            )
        )

        # Hard caps based on coverage.
        if ratio == 0:
            overall = min(
                overall,
                2
            )

        elif ratio < 0.25:
            overall = min(
                overall,
                4
            )

        elif ratio < 0.50:
            overall = min(
                overall,
                6
            )

        elif ratio < 0.75:
            overall = min(
                overall,
                8
            )

        strengths = []

        if ratio >= 0.50:

            if coverage["matched"]:

                strengths.append(
                    "Correctly covered: "
                    + ", ".join(
                        coverage["matched"][:5]
                    )
                    + "."
                )

        improvements = []

        if coverage["missing"]:

            improvements.append(
                "Explain the missing concept(s): "
                + ", ".join(
                    coverage["missing"][:5]
                )
                + "."
            )

        if not improvements:

            if overall >= 9:

                improvements.append(
                    "The answer is strong. Add a short practical example if appropriate."
                )

            else:

                improvements.append(
                    "Add a specific example to make the explanation stronger."
                )

        return {
            "overall_score": overall,
            "correctness": correctness,
            "relevance": relevance,
            "clarity": clarity,
            "completeness": completeness,
            "strengths": strengths,
            "improvements": improvements,
            "better_answer": ""
        }

    return None


# ============================================================
# AI FALLBACK FOR UNKNOWN QUESTIONS
# ============================================================

def _ai_evaluate_unknown(
    question,
    answer
):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict technical interview evaluator.\n\n"
                "Evaluate whether the candidate actually answers "
                "the exact question.\n\n"
                "Do not give a high score merely because the answer "
                "contains technical words.\n"
                "Unrelated answers must receive low relevance "
                "and low overall scores.\n"
                "Factually incorrect answers must receive low "
                "correctness.\n"
                "Partial answers should receive medium scores.\n\n"
                "Return ONLY valid JSON:\n"
                "{"
                "\"overall_score\":0,"
                "\"correctness\":0,"
                "\"relevance\":0,"
                "\"clarity\":0,"
                "\"completeness\":0,"
                "\"strengths\":[],"
                "\"improvements\":[],"
                "\"better_answer\":\"\""
                "}"
            )
        },
        {
            "role": "user",
            "content": (
                f"Question:\n{question}\n\n"
                f"Candidate answer:\n{answer}"
            )
        }
    ]

    raw = _generate(
        messages,
        300
    )

    try:

        return json.loads(
            raw
        )

    except json.JSONDecodeError:

        start = raw.find("{")
        end = raw.rfind("}")

        if (
            start != -1
            and end != -1
            and end > start
        ):

            try:

                return json.loads(
                    raw[
                        start:end + 1
                    ]
                )

            except json.JSONDecodeError:
                pass

    return {
        "overall_score": 0,
        "correctness": 0,
        "relevance": 0,
        "clarity": 0,
        "completeness": 0,
        "strengths": [],
        "improvements": [
            "The evaluator could not produce a valid evaluation."
        ],
        "better_answer": ""
    }


# ============================================================
# BETTER ANSWER
# ============================================================

def _generate_better_answer(
    question
):

    messages = [
        {
            "role": "system",
            "content": (
                "You are an interview coach.\n"
                "Give a concise and technically accurate answer "
                "to the interview question.\n"
                "Answer directly.\n"
                "Do not include labels or evaluation."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    return _generate(
        messages,
        180
    )


# ============================================================
# NORMALIZE EVALUATION
# ============================================================

def _normalize_evaluation(
    evaluation
):

    if not isinstance(
        evaluation,
        dict
    ):

        evaluation = {}

    score_fields = [
        "overall_score",
        "correctness",
        "relevance",
        "clarity",
        "completeness"
    ]

    for field in score_fields:

        try:

            value = int(
                evaluation.get(
                    field,
                    0
                )
            )

        except (
            TypeError,
            ValueError
        ):

            value = 0

        evaluation[field] = max(
            0,
            min(
                10,
                value
            )
        )

    strengths = evaluation.get(
        "strengths",
        []
    )

    if not isinstance(
        strengths,
        list
    ):

        strengths = []

    evaluation["strengths"] = [
        str(item).strip()
        for item in strengths
        if str(item).strip()
    ]

    improvements = evaluation.get(
        "improvements",
        []
    )

    if not isinstance(
        improvements,
        list
    ):

        improvements = []

    evaluation["improvements"] = [
        str(item).strip()
        for item in improvements
        if str(item).strip()
    ]

    better_answer = evaluation.get(
        "better_answer",
        ""
    )

    if not isinstance(
        better_answer,
        str
    ):

        better_answer = str(
            better_answer
        )

    evaluation["better_answer"] = (
        better_answer.strip()
    )

    return evaluation


# ============================================================
# PUBLIC: GENERATE ANSWER
# ============================================================

def generate_answer(
    question: str
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI Interview Coach. "
                "Give clear, accurate and concise answers "
                "suitable for a fresher technical interview."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    return _generate(
        messages,
        150
    )


# ============================================================
# PUBLIC: TEXT EVALUATION
# ============================================================

def evaluate_answer(
    question: str,
    answer: str
) -> str:

    evaluation = json_evaluate_answer(
        question,
        answer
    )

    return (
        f"Overall Score: "
        f"{evaluation['overall_score']}/10\n\n"
        f"Correctness: "
        f"{evaluation['correctness']}/10\n"
        f"Relevance: "
        f"{evaluation['relevance']}/10\n"
        f"Clarity: "
        f"{evaluation['clarity']}/10\n"
        f"Completeness: "
        f"{evaluation['completeness']}/10\n\n"
        f"Strengths:\n"
        + (
            "\n".join(
                f"- {item}"
                for item in evaluation["strengths"]
            )
            if evaluation["strengths"]
            else "- None identified."
        )
        + "\n\n"
        f"Improvements:\n"
        + "\n".join(
            f"- {item}"
            for item in evaluation["improvements"]
        )
        + "\n\n"
        f"Better Answer:\n"
        f"{evaluation['better_answer']}"
    )


# ============================================================
# PUBLIC: SCORE
# ============================================================

def score_answer(
    question: str,
    answer: str
) -> str:

    evaluation = json_evaluate_answer(
        question,
        answer
    )

    return (
        f"Score: "
        f"{evaluation['overall_score']}/10\n"
        f"Reason: "
        f"Correctness {evaluation['correctness']}/10, "
        f"Relevance {evaluation['relevance']}/10, "
        f"Completeness {evaluation['completeness']}/10."
    )


# ============================================================
# PUBLIC: STRUCTURED EVALUATION
# ============================================================

def structured_evaluate_answer(
    question: str,
    answer: str
) -> str:

    evaluation = json_evaluate_answer(
        question,
        answer
    )

    return (
        f"Overall Score: "
        f"{evaluation['overall_score']}/10\n"
        f"Correctness: "
        f"{evaluation['correctness']}/10\n"
        f"Relevance: "
        f"{evaluation['relevance']}/10\n"
        f"Clarity: "
        f"{evaluation['clarity']}/10\n"
        f"Completeness: "
        f"{evaluation['completeness']}/10\n\n"
        f"Strengths:\n"
        + (
            "\n".join(
                f"- {item}"
                for item in evaluation["strengths"]
            )
            if evaluation["strengths"]
            else "- None identified."
        )
        + "\n\n"
        f"Improvements:\n"
        + "\n".join(
            f"- {item}"
            for item in evaluation["improvements"]
        )
        + "\n\n"
        f"Better Answer:\n"
        f"{evaluation['better_answer']}"
    )


# ============================================================
# PUBLIC: JSON EVALUATION
# ============================================================

def json_evaluate_answer(
    question: str,
    answer: str
):

    # --------------------------------------------------------
    # Empty answer
    # --------------------------------------------------------

    if _is_empty_answer(answer):

        better = _generate_better_answer(
            question
        )

        return {
            "overall_score": 0,
            "correctness": 0,
            "relevance": 0,
            "clarity": 0,
            "completeness": 0,
            "strengths": [],
            "improvements": [
                "Provide an actual answer to the interview question."
            ],
            "better_answer": better
        }

    # --------------------------------------------------------
    # Don't know
    # --------------------------------------------------------

    if _is_dont_know_answer(answer):

        better = _generate_better_answer(
            question
        )

        return {
            "overall_score": 1,
            "correctness": 0,
            "relevance": 1,
            "clarity": 2,
            "completeness": 0,
            "strengths": [],
            "improvements": [
                "You did not provide a substantive answer.",
                "Learn the basic concept and explain it in your own words."
            ],
            "better_answer": better
        }

    # --------------------------------------------------------
    # Deterministic evaluation FIRST.
    # --------------------------------------------------------

    deterministic = _deterministic_evaluation(
        question,
        answer
    )

    if deterministic is not None:

        deterministic["better_answer"] = (
            _generate_better_answer(
                question
            )
        )

        return _normalize_evaluation(
            deterministic
        )

    # --------------------------------------------------------
    # AI fallback for questions without concepts.
    # --------------------------------------------------------

    evaluation = _ai_evaluate_unknown(
        question,
        answer
    )

    evaluation = _normalize_evaluation(
        evaluation
    )

    if not evaluation["better_answer"]:

        evaluation["better_answer"] = (
            _generate_better_answer(
                question
            )
        )

    if evaluation["overall_score"] < 5:

        evaluation["strengths"] = []

    if not evaluation["improvements"]:

        evaluation["improvements"] = [
            "Add the key technical concepts required by the question."
        ]

    return evaluation