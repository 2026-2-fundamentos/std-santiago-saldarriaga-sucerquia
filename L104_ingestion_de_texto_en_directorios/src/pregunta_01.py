import glob
import os
import pandas as pd


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "submission")

    os.makedirs(output_dir, exist_ok=True)

    splits = ["train", "test"]
    sentiments = ["negative", "neutral", "positive"]

    for split in sorted(splits):
        phrases = []
        targets = []

        for sentiment in sorted(sentiments):
            folder_path = os.path.join(data_dir, split, sentiment)

            file_paths = sorted(glob.glob(os.path.join(folder_path, "*.txt")))

            for file_path in file_paths:
                with open(file_path, "r", encoding="utf-8") as f:
                    phrase = f.read().strip()
                    phrases.append(phrase)
                    targets.append(sentiment)

        df = pd.DataFrame({"phrase": phrases, "target": targets})

        output_file = os.path.join(output_dir, f"{split}_dataset.csv")
        df.to_csv(output_file, index=False, encoding="utf-8")


if __name__ == "__main__":
    pregunta_01()