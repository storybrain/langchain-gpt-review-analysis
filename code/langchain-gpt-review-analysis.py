import asyncio
import nest_asyncio
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import create_async_playwright_browser
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
import os
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables from the .env file.
load_dotenv(find_dotenv())

# Allow nested async calls.
nest_asyncio.apply()


async def main():
    # Create an asynchronous browser instance using Playwright.
    async_browser = create_async_playwright_browser()

    # Get the browser toolkit which provides utility functions.
    toolkit = PlayWrightBrowserToolkit.from_browser(
        async_browser=async_browser)
    tools = toolkit.get_tools()

    # Create a dictionary for accessing tools by their name.
    tools_by_name = {tool.name: tool for tool in tools}
    navigate_tool = tools_by_name["navigate_browser"]
    get_elements_tool = tools_by_name["get_elements"]

    # Navigate to the Amazon product reviews URL.
    await navigate_tool.arun(
        {"url": "https://www.amazon.com/Charger-Certified-Adapter-Lightning-Compatible/product-reviews/B0BW5X89MM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"}
    )

    # Extract reviews from the webpage using the provided selector.
    elements = await get_elements_tool.arun(
        {"selector": ".review", "attributes": ["innerText"]}
    )

    # Define the template for the prompt.
    prompt_template = """
    From the reviews delimited by ```
    Provide a summary of reviews to find pros and cons of the product

    ```
    {reviews}
    ```
    """

    # Initialize the prompt template.
    prompt = PromptTemplate(
        template=prompt_template,   
        input_variables=["reviews"],
    )

    # Initialize the OpenAI Chat model.
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Create an extraction chain using the schema and the Chat model.
    chain = LLMChain(llm=llm, prompt=prompt)
    # Print the extracted results.
    print(chain.run(reviews=elements))

# Run the main asynchronous function.
asyncio.run(main())
