from deepscientist.factory import create_deepscientist


def main():

    agent = create_deepscientist()

    response = agent.invoke(
        "How do Yamanaka factors compare to small-molecule reprogramming for hepatocyte conversion?"
    )

    print(response)


if __name__ == "__main__":
    main()
