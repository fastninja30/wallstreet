import gpt_api


def extract_stock_symbols(comments):
    """
    Extracts stock symbols from a list of comments, using a prompt from a file.
    Args:
    - comments: List of strings, where each string is a comment or post.

    Returns:
    - A list of tuples, where each tuple contains the original comment and the extracted stock symbol.
    """
    extracted_data = []

    # Read the initial prompt from prompt.txt
    with open('prompt.txt', 'r') as file:
        base_prompt = file.read().strip()

    for comment in comments:
        # Use the base_prompt and append the specific comment to it.
        full_prompt = f"{base_prompt} {comment}"

        # Assuming gpt_api.get_response can be used like this.
        response, chat_history = gpt_api.get_response(full_prompt)
        stock_symbol = response.strip()  # Assuming the response is the stock symbol.

        extracted_data.append((comment, stock_symbol))

    return extracted_data


def analyze_comments(comments):
    """
    Args:
    - comments: List of strings, where each string is a comment or post to be analyzed.

    Returns:
    - A dictionary with stock symbols as keys and lists of scores as values.
    """
    scores_dict = {}  # Dictionary to store the results

    response, chat_history = gpt_api.get_response()
    for comment in comments:
        # Extract the stock symbol from the comment
        response, chat_history = gpt_api.get_response(f"News to Stock Symbol -- {comment}")
        stock_symbol = response.strip()  # Assuming the response is the stock symbol

        # Now, get the score for the comment
        score_response, score_chat_history = gpt_api.get_response(comment)
        score = score_response.strip()  # Assuming the response is the score

        # Update the dictionary with the score
        if stock_symbol in scores_dict:
            scores_dict[stock_symbol].append(score)
        else:
            scores_dict[stock_symbol] = [score]

    return scores_dict

