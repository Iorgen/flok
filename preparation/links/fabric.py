from preparation.links.creators import (
    TransportCharterCollectionLinksCreator, TransportCharterDetailLinksCreator,
    FindOrgCollectionLinksCreator, FindOrgPagesLinksCreator,
    KAgentPagesLinksCreator
)


class LinkCreatorFabric:

    @staticmethod
    def get_link_creator(_type: str, _source: str):
        if _type == "collection":
            if _source == "charter":
                return TransportCharterCollectionLinksCreator()
            if _source == 'find_org':
                return FindOrgCollectionLinksCreator()
            # if _source == 'k_agent':
            #     return K
        if _type == "page":
            if _source == "charter":
                return TransportCharterDetailLinksCreator()
            if _source == 'k_agent':
                return KAgentPagesLinksCreator
            if _source == 'find_org':
                return FindOrgPagesLinksCreator()
