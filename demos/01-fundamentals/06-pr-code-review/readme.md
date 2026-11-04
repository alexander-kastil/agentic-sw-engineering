# Pull Requests & Code Reviews


## Pull Request Support

GitHub Copilot assists with pull request workflows by automatically generating comprehensive PR descriptions based on your code changes. Copilot analyzes the diff and commit history to suggest clear, well-structured descriptions that summarize what changed, why, and the impact of the changes. This saves time on documentation and ensures consistency across your team's pull requests.

## Code Review Support

Copilot enhances code review processes by providing intelligent suggestions and feedback on code changes. During review, Copilot can identify potential issues, suggest improvements, explain complex logic, and recommend best practices. This helps reviewers catch bugs and inconsistencies more efficiently while also helping authors understand suggestions and improve code quality before merge.

## Agent merge: finishing the pull request

Opening a pull request is rarely the end of the work. Reviewers leave comments, checks fail, the base branch moves and creates merge conflicts, and a workflow needs a rerun. Agent merge hands that loop to an agent: it addresses review feedback, fixes failed checks and merge conflicts, and reruns workflows, and it repeats until the pull request is ready to merge. It has been available as a Preview since VS Code 1.136 and is controlled by the setting `chat.agentMerge.enabled`.

You turn it on per session, and only from the Agents window. Run **Enable Agent Merge for Active Session**, or select the **Agent Merge** button in the title bar. The agent works on the branch of that session, so the changes it pushes are visible in the pull request like any other commit. Each pass shows what it changed, which keeps every step of the loop reviewable.

Since VS Code 1.138 the Agents window also creates the pull request itself for Agent Host sessions, with one form. You review and edit the generated title and description, choose draft status and configure merge options, then create the pull request directly or send the request to the agent. The form remembers your options for the next time. The Agent Merge option in that form is experimental and appears only when `chat.agentMerge.enabled` is set.

The workflow therefore runs in one place: the agent writes the change, the form opens the pull request, and Agent merge carries it through review and checks. This pairs with the review support above, because review comments become the feedback the agent then addresses.

Ask yourself which feedback is routine, such as a renamed variable or a missing null check, and which needs a design decision; only the first kind should be delegated. Agent merge removes the waiting between a failed check and its fix, which is where pull requests usually stall for hours. You stay the approver: treat the loop as a fast first responder for routine feedback and read the final diff before you merge.

> Note: Agent merge and the pull request form are VS Code Agents window features. In Visual Studio and JetBrains IDEs, and on GitHub.com, use the pull request tools of that surface.

## Demo

1. Add the setting below to your user settings (JSON), open the Agents window, and start a session on a repository that has an open pull request with a failing check or a review comment. Then run **Enable Agent Merge for Active Session** (or select the **Agent Merge** button in the title bar).

   ```json
   { "chat.agentMerge.enabled": true }
   ```

   Expected result: the agent addresses the review comments and failed checks, reruns the workflows, and keeps going until the pull request is ready to merge.

## Links & Resources

- [Finish a pull request with Agent Merge](https://code.visualstudio.com/docs/agents/run/agents-window#_finish-a-pull-request-with-agent-merge) - enabling Agent merge per session and creating pull requests from the Agents window

[← Previous: Agent Mode Basics](../05-agent-mode-basics/readme.md) | [Back to Fundamentals](../readme.md) | [Next: Working in the Terminal →](../07-terminal/readme.md)
