import argparse

import pandas as pd
from sklearn.model_selection import train_test_split

from utils.util import set_unknown, load_data

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-i", "--input",
    default="dataset/face_encodings.csv",
    help="location of file to be splitted"
    )
ap.add_argument(
    "-r", "--train",
    default="dataset/face_encodings__train.csv",
    help="location of train file"
    )
ap.add_argument(
    "-e", "--test",
    default="dataset/face_encodings__test.csv",
    help="location of test file"
    )

args = vars(ap.parse_args())


# Load data
df = load_data(args['input']).drop(['Unnamed: 0'],axis=1)
print(df)
train, test = train_test_split(df, test_size=0.2)

print('total')
print(df['128'].value_counts()) # / len(df) * 100)

print('train')
print(train['128'].value_counts()) # / len(train) * 100)

print('test')
print(test['128'].value_counts()) # / len(test) * 100)

train.to_csv(args['train'], index=False)
test.to_csv(args['test'], index=False)