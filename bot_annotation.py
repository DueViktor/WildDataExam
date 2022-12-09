import pandas as pd


def is_ln_bot(string):
    if isinstance(string, float):
        return string
    if (
        "lntipbot" in string
        or "invoice" in string
        or "balance" in string
        or "deposit" in string
        or "withdraw" in string
        or "execute" in string
    ):
        return True
    else:
        return False


def is_company_bot(string):
    if isinstance(string, float):
        return string
    if "zelcore" in string:
        return True
    else:
        return False


def is_mod_bot(string):
    if isinstance(string, float):
        return string
    if "flagged for removal" in string or "i am a bot" in string:
        return True
    else:
        return False


def main():
    fpath = "data/final_datasets/"
    raw_data = pd.read_csv(fpath + "aggregated_dataset.csv", sep=";")
    raw_data["lnbot"] = raw_data["corpus"].apply(lambda x: is_ln_bot(x))
    raw_data["zelcore"] = raw_data["corpus"].apply(lambda x: is_company_bot(x))
    raw_data["mod"] = raw_data["corpus"].apply(lambda x: is_mod_bot(x))

    raw_data.to_csv(
        "data/final_datasets/bot_annotated_dataset.csv", index=None, sep=";"
    )


if __name__ == "__main__":
    main()
