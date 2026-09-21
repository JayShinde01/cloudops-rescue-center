const API_URL = "http://localhost:5000";

const incidentList = document.getElementById("incidentList");

const totalIncidents = document.getElementById("totalIncidents");
const openIncidents = document.getElementById("openIncidents");
const resolvedIncidents = document.getElementById("resolvedIncidents");

const incidentForm = document.getElementById("incidentForm");
const message = document.getElementById("message");


async function loadIncidents() {

    try {

        const response = await fetch(
            `${API_URL}/incidents`
        );

        const incidents = await response.json();

        displayIncidents(incidents);

    } catch (error) {

        incidentList.innerHTML =
            "<p>Unable to connect to Incident API.</p>";

        console.error(error);
    }
}


function displayIncidents(incidents) {

    totalIncidents.textContent = incidents.length;

    const open = incidents.filter(
        incident => incident.status === "OPEN"
    ).length;

    const resolved = incidents.filter(
        incident => incident.status === "RESOLVED"
    ).length;

    openIncidents.textContent = open;
    resolvedIncidents.textContent = resolved;


    if (incidents.length === 0) {

        incidentList.innerHTML =
            "<p>No incidents reported.</p>";

        return;
    }


    incidentList.innerHTML = incidents.map(
        incident => `

        <div class="incident">

            <h3>
                ${incident.id} - ${incident.title}
            </h3>

            <p>
                <strong>Severity:</strong>
                ${incident.severity}
            </p>

            <p>
                <strong>Status:</strong>
                ${incident.status}
            </p>

        </div>

        `
    ).join("");
}


incidentForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const title =
            document.getElementById("title").value;

        const severity =
            document.getElementById("severity").value;


        try {

            const response = await fetch(
                `${API_URL}/incidents`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        title: title,
                        severity: severity
                    })
                }
            );


            if (!response.ok) {
                throw new Error("Failed to create incident");
            }


            const incident = await response.json();

            message.textContent =
                `Incident ${incident.id} created successfully.`;

            message.style.color = "green";

            incidentForm.reset();

            await loadIncidents();


        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to create incident.";

            message.style.color = "red";
        }

    }
);


loadIncidents();