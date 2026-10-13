
import streamlit as st
import requests

st.set_page_config(
    page_title="Explore Artworks with MET Museum API",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Explore Artworks with MET Museum API")
st.write("Search artworks from The Metropolitan Museum of Art.")

keyword = st.text_input(
    "Enter an artwork, artist, or subject",
    value="flower"
)

if st.button("Search Artworks"):
    if keyword.strip():
        with st.spinner("Searching the museum collection..."):
            try:
                search_url = (
                    "https://collectionapi.metmuseum.org/public/collection/v1/search"
                )

                response = requests.get(
                    search_url,
                    params={"q": keyword, "hasImages": "true"},
                    timeout=20
                )
                response.raise_for_status()
                data = response.json()
                object_ids = data.get("objectIDs") or []

                if not object_ids:
                    st.warning("No artworks found. Try another keyword.")
                else:
                    st.success(f"Found {len(object_ids)} matching artworks.")
                    st.write("Showing up to 6 results.")

                    for object_id in object_ids[:6]:
                        detail_url = (
                            "https://collectionapi.metmuseum.org/public/collection/v1/objects/"
                            + str(object_id)
                        )
                        detail_response = requests.get(
                            detail_url, timeout=20
                        )
                        detail_response.raise_for_status()
                        artwork = detail_response.json()

                        st.subheader(
                            artwork.get("title") or "Untitled"
                        )

                        image_url = artwork.get("primaryImageSmall")
                        if image_url:
                            st.image(image_url, width=300)

                        st.write(
                            "**Artist:**",
                            artwork.get("artistDisplayName") or "Unknown"
                        )
                        st.write(
                            "**Date:**",
                            artwork.get("objectDate") or "Unknown"
                        )
                        st.write(
                            "**Medium:**",
                            artwork.get("medium") or "Not specified"
                        )

                        if artwork.get("objectURL"):
                            st.link_button(
                                "View on MET Museum website",
                                artwork["objectURL"]
                            )

                        st.divider()

            except requests.RequestException as error:
                st.error(f"Unable to connect to the MET API: {error}")
    else:
        st.warning("Please enter a search keyword.")
#
