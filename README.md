# Introduction

This is a cheker for finding the violation of new generated Mermaid Code.

In this repo, we will use __regex__ for analysing Mermaid code directly.

# TODO list:
- [ ] reading through the hard compiler passed Mermaid code (.mmd file) to locate each parts
    - [ ] node define part
    - [ ] type define part
    - [ ] node type assignment part
    - [ ] edge connection part

- [ ] read through __type__ definition to check the connection correctness
    - [ ] define type by config file (written by json)
    - [ ] read through the edge connection part to verify the connection correctness
        - [ ] W1: lack necessary input (W1 <-> Wrong 1)
        - [ ] W2: lack necessary output

> Those are the main mistake in our generated Mermaid workflow. Even though it can pass compiler by Mermaic, since it doesn't violate any grammer of Mermaid, but it still may not fully obey our setting of workflow which would mislead the python code.
