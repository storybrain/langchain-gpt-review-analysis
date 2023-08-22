import asyncio
import nest_asyncio
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import create_async_playwright_browser
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
import os
from dotenv import load_dotenv, find_dotenv

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
        {"url": "https://www.amazon.com/OnePlus-Unlocked-Android-Smartphone-Charging/product-reviews/B07XWGWPH5/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"}
    )

    # Extract reviews from the webpage using the provided selector.
    elements = await get_elements_tool.arun(
        {"selector": ".review", "attributes": ["innerText"]}
    )

    # Define the schema for the extracted reviews.
    schema = {
        "properties": {
            "name": {"type": "string"},
            "review": {"type": "string"},
            "rating": {"type": "integer"},
        },
        "required": ["name", "review", "rating"],
    }

    # Initialize the OpenAI Chat model.
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Create an extraction chain using the schema and the Chat model.
    chain = create_extraction_chain(schema, llm)

    # Print the extracted results.
    print(chain.run(elements))

# Run the main asynchronous function.
asyncio.run(main())
