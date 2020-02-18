import argparse
from pathlib import Path

import matplotlib as mpl
import pandas as pd

mpl.use("Agg")

from deep_sentinel import utils
from deep_sentinel.models import dnn

activation_funcs = dnn.model.utils.ActivationFunc.choices()


def get_parser():
    parser = argparse.ArgumentParser(description="Sample implementation to train the model"
                                                 " with subtilin production data")
    parser.add_argument("-i",
                        "--input-dir",
                        type=Path,
                        required=True,
                        help="Path to dir including train data")
    parser.add_argument("-o",
                        "--output-dir",
                        type=Path,
                        required=True,
                        help="Path to output dir")
    train_params = parser.add_argument_group("Train params")
    train_params.add_argument("-b",
                              "--batch-size",
                              type=int,
                              default=16,
                              help="Minibatch size")
    train_params.add_argument("-d",
                              "--device",
                              type=str,
                              default="-1",
                              help="Device ID to use (negative value indicate CPU)")
    train_params.add_argument("-e",
                              "--max-epoch",
                              type=int,
                              default=20,
                              help="Max epoch")
    train_params.add_argument("-r",
                              "--dropout-ratio",
                              type=float,
                              default=0.5,
                              help="Dropout ratio")
    model_params = parser.add_argument_group("Model params")
    model_params.add_argument("-n",
                              "--n-units",
                              type=int,
                              default=64,
                              help="Hidden size")
    model_params.add_argument("-l",
                              "--lstm-stack",
                              type=int,
                              default=1,
                              help="Number of stacked LSTM unit")
    model_params.add_argument("-p",
                              "--bprop-length",
                              type=int,
                              default=100,
                              help="Update parameters once with the specified number of data")
    model_params.add_argument("-a",
                              "--activation",
                              type=str,
                              choices=activation_funcs,
                              default=activation_funcs[0],
                              help="Which activation function to use "
                                   "({} are available)".format(activation_funcs))
    model_params.add_argument("-g",
                              "--gmm-classes",
                              type=int,
                              default=1,
                              help="Number of GMM classes")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    in_dir = utils.to_absolute(args.input_dir)
    if not in_dir.exists():
        print("{} does not exist.".format(in_dir))
        exit(1)

    train_csv = in_dir / "subtilin-training.csv"
    if not train_csv.exists():
        print("{} does not exist. Please generate training data.".format(train_csv))
        exit(1)

    out_dir = utils.mkdir(args.output_dir)

    print("----- Model Params -----")
    print("Minibatch: {}".format(args.batch_size))
    print("N units: {}".format(args.n_units))
    print("LSTM Stack: {}".format(args.lstm_stack))
    print("Back propagation length: {}".format(args.bprop_length))
    print("Activation Function: {}".format(args.activation))
    print("GMM Classes: {}".format(args.gmm_classes))

    # Create model instance
    dnn_model = dnn.DNN(
        batch_size=args.batch_size,
        output_dir=out_dir,
        max_epoch=args.max_epoch,
        device=args.device,
        n_units=args.n_units,
        lstm_stack=args.lstm_stack,
        dropout_ratio=args.dropout_ratio,
        activation=args.activation,
        bprop_length=args.bprop_length,
        gmm_classes=args.gmm_classes
    )
    # Read CSV data and convert it to pandas.DataFrame
    train_data = pd.read_csv(str(train_csv), index_col=[0], header=[0])
    print("----- Train data -----")
    print("File: {}".format(train_csv))
    print("Length: {}".format(len(train_data)))
    print("Number of features: {}".format(len(train_data.columns)))

    print("----- Train info -----")
    print("Max epoch: {}".format(args.max_epoch))
    print("Device ID: {}".format(args.device))
    print("Dropout ratio: {}".format(args.dropout_ratio))
    print("Output dir: {}".format(out_dir))

    # Train the model with given data
    print("----- Start to train -----")
    dnn_model.fit(train_data)
    # Dump the weights of the model whose performance is the best.
    saved_model = dnn_model.save(out_dir)
    print("Save as: {}".format(saved_model))
    print("----- End -----")


if __name__ == "__main__":
    main()
