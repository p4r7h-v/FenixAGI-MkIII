// initialize messages array
let messages = [{ role: "system", content: "You are a helpful assistant" }];    

// This function is responsible for displaying the user's message on the screen and calling the getChatResponse function to get a response from GPT.
async function displayMessage() {
    // Get the user's input from the message-input element
    const userInput = document.getElementById("message-input").value;
    // Get the main section element
    const mainSection = document.getElementById("main-section");

    // Create a new paragraph element to display the user's message
    const userMessageElement = document.createElement("p");
    userMessageElement.innerText = userInput;
    userMessageElement.classList.add("bg-gray-400", "rounded-lg", "shadow-md", "p-4", "mx-auto", "my-4", "max-w-md" );
    userMessageElement.style.color = "black";
    // Before appending the user's message, check if the user is already near the bottom
    let shouldScroll = mainSection.scrollTop + mainSection.clientHeight >= mainSection.scrollHeight - 40; // 20 is a small buffer

    // Append the user's message element to the main section
    mainSection.appendChild(userMessageElement);

    // If the user was already near the bottom, scroll to the bottom
    if (shouldScroll) {
        mainSection.scrollTop = mainSection.scrollHeight;
    }

 

    // Scroll to the bottom of the main section
    mainSection.scrollTop = mainSection.scrollHeight;

    // Add the user's message to the messages array
    messages.push({ role: "user", content: userInput });

    // Call the getChatResponse function to get a response from GPT
    await getChatResponse(userInput, mainSection);
    // Clear the input box
    document.getElementById("message-input").value = "";
    
}

// Add an event listener to the display-message-button element to call the displayMessage function when the button is clicked
const messageInput = document.getElementById("message-input");

// shift + enter to add new line or enter to send message
messageInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        displayMessage();
    }
});

// Add an event listener to the display-message-button element to call the displayMessage function when the button is clicked
const displayMessageButton = document.getElementById("display-message-button");
displayMessageButton.addEventListener("click", displayMessage);

// Set the OpenAI API key
const YOUR_API_KEY = "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";

// Set the OpenAI API URL
const API_URL = "https://api.openai.com/v1/chat/completions";



// This function sends a request to the OpenAI API to get a response from GPT.
async function getChatResponse(promptInput, mainSection) {
    try {
        // Send a POST request to the OpenAI API with the user's input and API key
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${YOUR_API_KEY}`,
            },
            body: JSON.stringify({
                model: "gpt-3.5-turbo",
                messages: messages,
                stream: true,
            }),
        });

        // Create a reader to read the response body as a stream
        const reader = response.body.getReader();
        // Create a decoder to decode the response body as UTF-8
        const decoder = new TextDecoder("utf-8");

        // Initialize variables to store the assistant's message and message element
        let assistantMessage = "";
        let assistantMessageElement;

        // Read the response body as a stream and parse the JSON data
        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                break;
            }

            // Decode the value of the response body as UTF-8
            const chunk = decoder.decode(value);
            // Split the decoded chunk into an array of lines
            const lines = chunk.split("\n");

            // Loop through each line in the array of lines
            for (const line of lines) {
                // Remove any leading "data: " and trim the line
                const cleanedLine = line.replace(/^data: /, "").trim();
                // If the cleaned line is '[DONE]', skip to the next iteration of the loop
                if (cleanedLine === '[DONE]') continue;
                // If the cleaned line is empty, skip to the next iteration of the loop
                if (cleanedLine.trim().length === 0) {
                    continue;
                }

                try {
                    // Parse the cleaned line as JSON
                    const parsedLine = JSON.parse(cleanedLine);
                    // If the parsed line has choices and the length of the choices array is greater than 0
                    if (parsedLine.choices && parsedLine.choices.length > 0) {
                        // Get the first choice from the choices array
                        const choice = parsedLine.choices[0];
                        // If the choice has a delta and the delta has content
                        if (choice.delta && choice.delta.content) {
                            // Append the assistant's message to the assistantMessage variable
                            assistantMessage += choice.delta.content;
                            // Create a new paragraph element to display the assistant's message if it doesn't exist
                            if (!assistantMessageElement) {
                                assistantMessageElement = document.createElement("p");
                                assistantMessageElement.classList.add("bg-gray-300", "rounded-lg", "shadow-md", "p-4", "mx-auto", "my-4", "max-w-md");
                                mainSection.appendChild(assistantMessageElement);

                                // Add the assistant's message to the messages array
                                messages.push({ role: "assistant", content: assistantMessage });
                            }

                            // Before updating the assistant's message, check if the user is already near the bottom
                            shouldScroll = mainSection.scrollTop + mainSection.clientHeight >= mainSection.scrollHeight - 40; // 20 is a small buffer 
                            // Update the innerText of the assistant's message element
                            assistantMessageElement.innerText = assistantMessage;
                            // If the user was already near the bottom, scroll to the bottom
                            if (shouldScroll) {
                                mainSection.scrollTop = mainSection.scrollHeight;
                            }
                        }
                        if (choice.finish_reason) {
                            console.log("Assistant Message: ", assistantMessage);
                            // Reset the assistantMessage and assistantMessageElement variables for the next complete message
                            assistantMessage = "";
                            assistantMessageElement = null;
                        }
                    }
                } catch (error) {
                    if (error instanceof SyntaxError) {
                        console.error("Failed to parse JSON:", cleanedLine, error);
                    } else {
                        throw error;
                    }
                }
            }
        }
    } catch(error) {
        console.error("Error:", error);
    }
}