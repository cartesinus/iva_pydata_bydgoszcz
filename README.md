# Brain in a Jar, or Modern Virtual Assistants: Exploring the Evolution of NLU in Virtual Assistants

This is a repository with code for presentation about Virtual Assistants I gave on PyData Bydgoszcz in November 2023.

[Link to presentation](https://docs.google.com/presentation/d/1LuZWLnnlX1ke2rY51DiydDOT0OPcUwZ0CA4QpoXHFWc/edit?usp=sharing)

### Joint NLU Live Coding

Follow these steps to reproduce the Natural Language Understanding (NLU) model training from our recent PyData event session.

1. **Environment Setup**
   - Create a Conda environment:
     ```
     conda create --name joint_nlu python=3.10
     ```
   - Activate the environment:
     ```
     conda activate joint_nlu
     ```
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
     Alternatively, this step can be integrated into the environment creation process.

2. **Grammar Modification**
   - Navigate to the grammars directory:
     ```
     cd grammars/
     ```
   - Modify the `calendar.gram` file as desired.

3. **Grammar Expansion**
   - Expand the grammars into corpora:
     ```
     python generate_patterns.py -f calendar.gram > iva-calendar-0.1.0.tsv
     ```
   - Fix two common errors:
     1. Remove double underscores (`"__"`). This can be done manually or using `sed`:
        ```
        sed -i 's/__//g' calendar.gram
        ```
     2. Eliminate spaces surrounding tabs. Replace `(space)(tab)(space)` with `(tab)`.

4. **Slot Expansion**
   - Run the slot expansion script:
     ```
     ./expand-slots.sh iva-calendar-0.1.0.tsv iva-corpus-calendar-0.1.0.tsv true true
     ```

5. **Configuration Adjustments**
   - Modify the `join_nlu` configuration in `joint_nlu/calendar.json`. Experiment with the `num_train_epochs` setting as needed.

6. **Corpus File Naming**
   - Ensure your corpus file name matches the `_URL` in `custom.py`.

7. **Model Training on Google Colab**
   - Import `joint_nlu_train_on_colab.ipynb` into Google Colab and follow the instructions therein.
   - After cloning the `joint_nlu` repository in Colab, upload three files into the `joint_nlu` directory: `calendar.json`, the corpus file, and `custom.py`.
   - Proceed with the training.

Upon successful completion, assuming `"push_to_hub": true` is set in `calendar.json`, your model will be uploaded to your Hugging Face Hub. For deployment and usage, refer to the [Joint NLU Repository](https://github.com/cartesinus/joint_nlu).
