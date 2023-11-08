import { Pivot, PivotItem } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./AnalysisPanel.module.css";

import { SupportingContent } from "../SupportingContent";
import { ChatAppResponse } from "../../api";
import { AnalysisPanelTabs } from "./AnalysisPanelTabs";

interface Props {
    className: string;
    activeTab: AnalysisPanelTabs;
    onActiveTabChanged: (tab: AnalysisPanelTabs) => void;
    activeCitation: string | undefined;
    activeFileName: string | undefined;
    activeWebURL: string | undefined;
    citationHeight: string;
    answer: ChatAppResponse;
}

const pivotItemDisabledStyle = { disabled: true, style: { color: "grey" } };

export const AnalysisPanel = ({ answer, activeTab, activeCitation, activeFileName, activeWebURL, citationHeight, className, onActiveTabChanged }: Props) => {
    const isDisabledThoughtProcessTab: boolean = !answer.choices[0].context.thoughts;
    const isDisabledSupportingContentTab: boolean = !answer.choices[0].context.data_points.length;
    const isDisabledCitationTab: boolean = !activeCitation;

    const sanitizedThoughts = DOMPurify.sanitize(answer.choices[0].context.thoughts!);

    const switchIframeURLByFileType = () => {
        if (!activeFileName) {
            return ''
        }

        const pathWithoutLastSegment = activeWebURL?.split('/').slice(0, -2).join('/');
        
        const fileExtension = activeFileName.split('.').pop()?.toLowerCase();
        switch (fileExtension) {
            case 'pptx':
                return `https://m365x52168024.sharepoint.com/_layouts/15/Doc.aspx?sourcedoc={${activeCitation}}&action=embedview&wdAr=1.7777777777777777`;
            case 'xlsx':
                return `${pathWithoutLastSegment}/_layouts/15/Doc.aspx?sourcedoc={${activeCitation}}&action=embedview&wdAllowInteractivity=False&wdDownloadButton=True&wdInConfigurator=True&wdInConfigurator=True`
            case 'docx':
                return `${pathWithoutLastSegment}/_layouts/15/Doc.aspx?sourcedoc={${activeCitation}}&action=embedview`
            case 'pdf':
                return `${pathWithoutLastSegment}/_layouts/15/embed.aspx?UniqueId=${activeCitation}`
            default:
                return '';
        }
    }
    

    return (
        <Pivot
            className={className}
            selectedKey={activeTab}
            onLinkClick={pivotItem => pivotItem && onActiveTabChanged(pivotItem.props.itemKey! as AnalysisPanelTabs)}
        >
            <PivotItem
                itemKey={AnalysisPanelTabs.ThoughtProcessTab}
                headerText="Thought process"
                headerButtonProps={isDisabledThoughtProcessTab ? pivotItemDisabledStyle : undefined}
            >
                <div className={styles.thoughtProcess} dangerouslySetInnerHTML={{ __html: sanitizedThoughts }}></div>
            </PivotItem>
            <PivotItem
                itemKey={AnalysisPanelTabs.SupportingContentTab}
                headerText="Supporting content"
                headerButtonProps={isDisabledSupportingContentTab ? pivotItemDisabledStyle : undefined}
            >
                <SupportingContent supportingContent={answer.choices[0].context.data_points} />
            </PivotItem>
            <PivotItem
                itemKey={AnalysisPanelTabs.CitationTab}
                headerText="Citation"
                headerButtonProps={isDisabledCitationTab ? pivotItemDisabledStyle : undefined}
            >
                {/* TODO: パワポ以外のファイルにも対応する */}
                <iframe 
                        src={switchIframeURLByFileType()}
                        width="100%" 
                        height="810px"
                    >
                        This is an embedded
                        <a target="_blank" href="https://office.com">
                            Microsoft Office
                        </a> 
                            powered by 
                        <a target="_blank" href="https://office.com/webapps">
                            Office
                        </a>
                        .
                    </iframe>
            </PivotItem>
        </Pivot>
    );
};
