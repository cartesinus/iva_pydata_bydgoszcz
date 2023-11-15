# NLU Grammars

Here is how you can create tsv corpus that after reformating to transformers can be used to train Joint NLU.

## How to generate corpus

```bash
mkdir -p data
python generate_patterns.py -f calendar.gram > data/iva_calendar-en_US-0.1.0-20231112.tsv
./expand-slots.sh data/iva_calendar-en_US-0.1.0-20231112.tsv data/iva_calendar-corpora-en_US-0.1.0-20231112.tsv true true
```

## How to train Joint NLU model
Refer to [Joint NLU](https://github.com/cartesinus/joint_nlu)
