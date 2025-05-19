# Introduction

This is a cheker for finding the violation of new generated Mermaid Code.

In this repo, we will use __regex__ for analysing Mermaid code directly.

# TODO list:
- [x] reading through the hard compiler passed Mermaid code (.mmd file) to locate each parts
    - [x] node define part
    - [x] type define part
    - [x] node type assignment part
    - [x] edge connection part
    - [x] comments part
    - [x] empty part (doesn't have any content)

- [x] read through __type__ definition to check the connection correctness
    - [x] define type by config file (written by json)
    - [x] read through the edge connection part to verify the connection correctness
        - [x] W1: check for PROBLEM and RETURN nodes existence
        - [x] W2: ensure all nodes have path to connect to both PROBLEM and RETURN
        - [x] W3: verify PROBLEM and RETURN nodes are of Interface class type
        - [x] W4: validate all nodes have legal node types from configuration
        - [x] W5: ensure ScEnSembleOp nodes have at least 2 incoming connections

> Those are the main mistake in our generated Mermaid workflow. Even though it can pass compiler by Mermaic, since it doesn't violate any grammer of Mermaid, but it still may not fully obey our setting of workflow which would mislead the python code.
