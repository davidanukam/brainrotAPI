const defaultName = "Empty";
const defaultDes = "Empty";
const defaultImage = "/images/default_brainrot_image.jpg";

const brainrotNameEl = document.getElementById("brainrotName");
const brainrotDesEl = document.getElementById("brainrotDes");
const brainrotImageEl = document.getElementById("brainrotImage");

async function loadFirstBrainrot() {
  try {
    const res = await fetch("http://127.0.0.1:8000/brainrots/");

    if (!res.ok) throw new Error("Failed to fetch brainrots");

    const brainrots = await res.json();

    if (brainrots.length == 0) {
      console.log("No Brainrots Found!");
      if (brainrotImageEl) {
        brainrotImageEl.style.backgroundImage = `url("${defaultImage}")`;
      }
    }

    const name = brainrots[0]?.name || defaultName;
    const description = brainrots[0]?.description || defaultDes;
    const imageUrl = brainrots[0]?.image || defaultImage;

    if (brainrotNameEl) {
      brainrotNameEl.textContent = `${name}`;
    }

    if (brainrotDesEl) {
      brainrotDesEl.textContent = `${description}`;
    }

    if (brainrotImageEl) {
        brainrotImageEl.style.backgroundImage = `url("${imageUrl}")`;
    }
  } catch (e) {
    console.error("Error fetching first brainrot:", e);

    if (brainrotImageEl) {
      brainrotImageEl.style.backgroundImage = `url("${defaultImage}")`;
    }
  }
}

document.addEventListener("DOMContentLoaded", loadFirstBrainrot);
