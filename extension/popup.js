// popup.js

// Obtain OAuth token using chrome.identity
function getAuthToken(interactive = true) {
    return new Promise((resolve, reject) => {
      chrome.identity.getAuthToken({ interactive }, token => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve(token);
        }
      });
    });
  }
  
  // Fetch a single page of messages (maxResults=100)
  async function listMessagesPage(token, pageToken = null) {
    let url = "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=100";
    if (pageToken) {
      url += "&pageToken=" + pageToken;
    }
    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!response.ok) {
      const errText = await response.text();
      throw new Error("Error fetching messages: " + errText);
    }
    return await response.json();
  }
  
  // Fetch all messages using pagination
  async function fetchAllMessages(token) {
    let allMessages = [];
    let pageToken = null;
    do {
      const data = await listMessagesPage(token, pageToken);
      if (data.messages) {
        allMessages = allMessages.concat(data.messages);
      }
      pageToken = data.nextPageToken;
    } while (pageToken);
    return allMessages;
  }
  
  // Retrieve labels from Gmail
  async function listLabels(token) {
    const response = await fetch(
      "https://gmail.googleapis.com/gmail/v1/users/me/labels",
      { headers: { Authorization: `Bearer ${token}` } }
    );
    if (!response.ok) {
      const errText = await response.text();
      throw new Error("Error fetching labels: " + errText);
    }
    const data = await response.json();
    console.log("Retrieved labels:", data.labels);
    if (!Array.isArray(data.labels)) {
      throw new Error("Expected labels to be an array, got: " + JSON.stringify(data.labels));
    }
    return data.labels;
  }
  
  // Create a label if it doesn't exist
  async function createLabel(token, labelName) {
    const response = await fetch(
      "https://gmail.googleapis.com/gmail/v1/users/me/labels",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          name: labelName,
          labelListVisibility: "labelShow",
          messageListVisibility: "show"
        })
      }
    );
    if (!response.ok) {
      const errText = await response.text();
      throw new Error("Error creating label '" + labelName + "': " + errText);
    }
    const data = await response.json();
    console.log(`Created label "${labelName}" with ID:`, data.id);
    return data.id;
  }
  
  // Add a label to a message
  async function addLabelToMessage(token, messageId, labelId) {
    const response = await fetch(
      `https://gmail.googleapis.com/gmail/v1/users/me/messages/${messageId}/modify`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ addLabelIds: [labelId] })
      }
    );
    if (!response.ok) {
      const errText = await response.text();
      throw new Error("Error modifying message " + messageId + ": " + errText);
    }
    return await response.json();
  }
  
  // Fetch the message snippet for classification
  async function getMessageSnippet(token, messageId) {
    const response = await fetch(
      `https://gmail.googleapis.com/gmail/v1/users/me/messages/${messageId}?format=full`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    if (!response.ok) {
      const errText = await response.text();
      throw new Error("Error fetching message details for " + messageId + ": " + errText);
    }
    const data = await response.json();
    return data.snippet || "";
  }
  
  // Asynchronously classify the email based on its snippet
  async function classifyEmail(token, messageId) {
    try {
      const snippet = await getMessageSnippet(token, messageId);
      const lowerSnippet = snippet.toLowerCase();
      if (lowerSnippet.includes("congratulations") || lowerSnippet.includes("excited to announce")) {
        return "successful";
      } else if (lowerSnippet.includes("regret to") || lowerSnippet.includes("other candidates")) {
        return "unsuccessful";
      } else if (lowerSnippet.includes("submitted")) {
        return "submitted";
      } else {
        return null; // Skip emails that don't match any category
      }
    } catch (error) {
      console.error("Error classifying message " + messageId + ": ", error);
      return null;
    }
  }
  
  document.getElementById('classifyAll').addEventListener('click', async () => {
    const resultsDiv = document.getElementById('results');
    
    // Default required labels mapping (only for messages that will be categorized)
    const requiredLabels = {
      successful: "successful_emails",
      unsuccessful: "unsuccessful_emails",
      submitted: "submitted_emails"
    };
  
    resultsDiv.innerText = 'Authenticating...';
    
    try {
      // Get OAuth token
      const token = await getAuthToken();
      resultsDiv.innerText = 'Fetching all messages...';
      const messages = await fetchAllMessages(token);
      console.log(`Total messages fetched: ${messages.length}`);
      
      // Retrieve current labels and ensure the required ones exist
      const labels = await listLabels(token);
      const labelMap = {};
      for (const [category, labelName] of Object.entries(requiredLabels)) {
        let labelObj = labels.find(l => l.name && l.name.toLowerCase() === labelName.toLowerCase());
        if (labelObj) {
          labelMap[category] = labelObj.id;
        } else {
          resultsDiv.innerText = `Creating label: ${labelName}`;
          const newLabelId = await createLabel(token, labelName);
          labelMap[category] = newLabelId;
        }
      }
      
      // Process every message in the mailbox.
      let processedCount = 0;
      for (const message of messages) {
        // Classify the email using its snippet.
        const category = await classifyEmail(token, message.id);
        if (!category) {
          // Skip messages that don't match any category
          continue;
        }
        const labelId = labelMap[category];
        if (!labelId) {
          console.error(`Label ID not found for category: ${category}. Skipping message ${message.id}`);
          continue;
        }
        await addLabelToMessage(token, message.id, labelId);
        processedCount++;
      }
      
      resultsDiv.innerText = `Processed ${processedCount} messages.`;
    } catch (error) {
      const errorDetails = error && error.message ? error.message : JSON.stringify(error);
      resultsDiv.innerText = 'Error: ' + errorDetails;
      console.error('Error details:', error);
    }
  });
  