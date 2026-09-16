[1mdiff --git a/ai_lab/phase_01_llm/__pycache__/agent.cpython-314.pyc b/ai_lab/phase_01_llm/__pycache__/agent.cpython-314.pyc[m
[1mindex 8a362d2..b08056e 100644[m
Binary files a/ai_lab/phase_01_llm/__pycache__/agent.cpython-314.pyc and b/ai_lab/phase_01_llm/__pycache__/agent.cpython-314.pyc differ
[1mdiff --git a/ai_lab/phase_01_llm/__pycache__/test_agent.cpython-314-pytest-9.1.1.pyc b/ai_lab/phase_01_llm/__pycache__/test_agent.cpython-314-pytest-9.1.1.pyc[m
[1mindex 76ca0ef..37a2b2f 100644[m
Binary files a/ai_lab/phase_01_llm/__pycache__/test_agent.cpython-314-pytest-9.1.1.pyc and b/ai_lab/phase_01_llm/__pycache__/test_agent.cpython-314-pytest-9.1.1.pyc differ
[1mdiff --git a/ai_lab/phase_01_llm/__pycache__/tools.cpython-314.pyc b/ai_lab/phase_01_llm/__pycache__/tools.cpython-314.pyc[m
[1mindex a09d3dc..8e673a9 100644[m
Binary files a/ai_lab/phase_01_llm/__pycache__/tools.cpython-314.pyc and b/ai_lab/phase_01_llm/__pycache__/tools.cpython-314.pyc differ
[1mdiff --git a/ai_lab/phase_01_llm/agent.py b/ai_lab/phase_01_llm/agent.py[m
[1mindex 26ae94a..ab9ecc0 100644[m
[1m--- a/ai_lab/phase_01_llm/agent.py[m
[1m+++ b/ai_lab/phase_01_llm/agent.py[m
[36m@@ -4,37 +4,75 @@[m [mfrom ai_lab.phase_01_llm.tools import get_sauce_demo_status[m
 [m
 def run_agent(user_prompt: str) -> str:[m
     """[m
[31m-    Simple educational python agent.[m
[32m+[m[32m    Simple educational Python agent.[m
 [m
     The LLM decides whether the request requires[m
     the Sauce Demo status tool.[m
     """[m
 [m
     decision_prompt = f"""[m
[31m-You are a simple routing agent.[m
[32m+[m[32mYou are a routing agent.[m
 [m
[31m-User request:[m
[31m-{user_prompt}[m
[32m+[m[32mYour job is to decide whether the user's question[m
[32m+[m[32mrequires calling the Sauce Demo status tool.[m
[32m+[m
[32m+[m[32mThe available tool is:[m
 [m
[31m-Decide what action is required.[m
[32m+[m[32mget_sauce_demo_status[m
[32m+[m[32m- Returns the current availability status of the Sauce Demo application.[m
 [m
[31m-If the user is asking about the availability or status[m
[31m-of Sauce Demo, respond with exactly:[m
[32m+[m[32mRULES:[m
[32m+[m
[32m+[m[32m1. If the user asks about Sauce Demo availability, status,[m
[32m+[m[32m   whether Sauce Demo is available, or whether Sauce Demo is up,[m
[32m+[m[32m   respond with exactly:[m
 [m
 USE_TOOL[m
 [m
[31m-Otherwise respond with exactly:[m
[32m+[m[32m2. For every other question, respond with exactly:[m
 [m
 ANSWER[m
[32m+[m
[32m+[m[32mExamples:[m
[32m+[m
[32m+[m[32mUser: Is Sauce Demo available?[m
[32m+[m[32mResponse: USE_TOOL[m
[32m+[m
[32m+[m[32mUser: Is Sauce Demo up?[m
[32m+[m[32mResponse: USE_TOOL[m
[32m+[m
[32m+[m[32mUser: What is the status of Sauce Demo?[m
[32m+[m[32mResponse: USE_TOOL[m
[32m+[m
[32m+[m[32mUser: What is Playwright?[m
[32m+[m[32mResponse: ANSWER[m
[32m+[m
[32m+[m[32mUser: Explain Python.[m
[32m+[m[32mResponse: ANSWER[m
[32m+[m
[32m+[m[32mDo not provide any explanation.[m
[32m+[m[32mDo not provide any other text.[m
[32m+[m
[32m+[m[32mUser request:[m
[32m+[m[32m{user_prompt}[m
[32m+[m
[32m+[m[32mDecision:[m
 """[m
 [m
     decision = generate_response_local(decision_prompt).strip()[m
[32m+[m
     print("\nAgent Decision:")[m
     print(repr(decision))[m
 [m
     if decision == "USE_TOOL":[m
[32m+[m[32m        print("\nExecuting Tool:")[m
[32m+[m[32m        print("get_sauce_demo_status")[m
[32m+[m
         tool_result = get_sauce_demo_status()[m
 [m
[32m+[m[32m        print("\nTool Result:")[m
[32m+[m[32m        print(tool_result)[m
[32m+[m
         final_prompt = f"""[m
 Answer the user's question using the tool result below.[m
 [m
[36m@@ -47,6 +85,18 @@[m [mTool result:[m
 Give a concise answer.[m
 """[m
 [m
[31m-        return generate_response_local(final_prompt)[m
[32m+[m[32m        final_response = generate_response_local(final_prompt)[m
[32m+[m
[32m+[m[32m        print("\nFinal Answer:")[m
[32m+[m[32m        print(final_response)[m
[32m+[m
[32m+[m[32m        return final_response[m
[32m+[m
[32m+[m[32m    print("\nNo tool required.")[m
[32m+[m
[32m+[m[32m    final_response = generate_response_local(user_prompt)[m
[32m+[m
[32m+[m[32m    print("\nFinal Answer:")[m
[32m+[m[32m    print(final_response)[m
 [m
[31m-    return generate_response_local(user_prompt)[m
\ No newline at end of file[m
[32m+[m[32m    return final_response[m
\ No newline at end of file[m
[1mdiff --git a/ai_lab/phase_01_llm/test_agent.py b/ai_lab/phase_01_llm/test_agent.py[m
[1mindex c79fd38..0e6217a 100644[m
[1m--- a/ai_lab/phase_01_llm/test_agent.py[m
[1m+++ b/ai_lab/phase_01_llm/test_agent.py[m
[36m@@ -1,12 +1,17 @@[m
 from ai_lab.phase_01_llm.agent import run_agent[m
 [m
[31m-[m
 def test_agent_uses_sauce_demo_tool():[m
[31m-    response = run_agent([m
[31m-        "Is the Sauce Demo application available?"[m
[31m-    )[m
[32m+[m[32m    user_prompt = "Is Sauce Demo available?"[m
[32m+[m
[32m+[m[32m    response = run_agent(user_prompt)[m
 [m
     assert response[m
[32m+[m[32m    assert "Sauce Demo" in response[m
[32m+[m
[32m+[m[32mdef test_agent_answers_without_tool():[m
[32m+[m[32m    user_prompt = "What is Playwright?"[m
 [m
[31m-    print("\nAgent Response:")[m
[31m-    print(response)[m
\ No newline at end of file[m
[32m+[m[32m    response = run_agent(user_prompt)[m
[32m+[m
[32m+[m[32m    assert response[m
[32m+[m[32m    assert "Playwright" in response[m
\ No newline at end of file[m
[1mdiff --git a/pages/ai_lab/phase_01_llm/README.md b/pages/ai_lab/phase_01_llm/README.md[m
[1mdeleted file mode 100644[m
[1mindex e69de29..0000000[m
[1mdiff --git a/pages/ai_lab/phase_01_llm/cloud_api.py b/pages/ai_lab/phase_01_llm/cloud_api.py[m
[1mdeleted file mode 100644[m
[1mindex e69de29..0000000[m
[1mdiff --git a/pages/ai_lab/phase_01_llm/local_ollama.py b/pages/ai_lab/phase_01_llm/local_ollama.py[m
[1mdeleted file mode 100644[m
[1mindex e69de29..0000000[m
