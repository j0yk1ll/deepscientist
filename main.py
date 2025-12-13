def main():
    from deepscientist.orchestrator import create_orchestrator_agent

    agent = create_orchestrator_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "How do Yamanaka factors compare to small-molecule reprogramming for hepatocyte conversion?",
                }
            ]
        }
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
