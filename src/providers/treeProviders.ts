import * as vscode from 'vscode';
import { CodeFlowIssue, CodeFlowMetrics, PerformanceHistory } from '../types';
import { DataService } from '../services/dataService';

// Tree Items
export class CodeFlowIssueItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly issue?: CodeFlowIssue
    ) {
        super(label, collapsibleState);
        
        if (issue) {
            this.tooltip = `${issue.file}:${issue.line}:${issue.column} - ${issue.message}`;
            this.description = `${issue.tool} - ${issue.severity}`;
            
            // Set icon based on severity
            switch (issue.severity) {
                case 'error':
                    this.iconPath = new vscode.ThemeIcon('error');
                    break;
                case 'warning':
                    this.iconPath = new vscode.ThemeIcon('warning');
                    break;
                case 'info':
                    this.iconPath = new vscode.ThemeIcon('info');
                    break;
            }
        }
    }
}

export class CodeFlowMetricsItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly value?: number,
        public readonly unit?: string
    ) {
        super(label, collapsibleState);
        
        if (value !== undefined) {
            this.description = unit ? `${value}${unit}` : value.toString();
        }
    }
}

export class CodeFlowHistoryItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly record?: PerformanceHistory
    ) {
        super(label, collapsibleState);
        
        if (record) {
            this.tooltip = `Duration: ${record.duration}ms, Issues: ${record.issues_found}, Fixed: ${record.issues_fixed}`;
            this.description = record.success ? '✅ Success' : '❌ Failed';
            this.iconPath = new vscode.ThemeIcon(record.success ? 'check' : 'error');
        }
    }
}

// Tree Data Providers
export class CodeFlowIssuesProvider implements vscode.TreeDataProvider<CodeFlowIssueItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<CodeFlowIssueItem | undefined | null | void> = new vscode.EventEmitter<CodeFlowIssueItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<CodeFlowIssueItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private dataService: DataService;

    constructor() {
        this.dataService = DataService.getInstance();
    }

    getTreeItem(element: CodeFlowIssueItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: CodeFlowIssueItem): Promise<CodeFlowIssueItem[]> {
        if (element) {
            // Return child issues for grouped items
            return this.getChildIssues(element);
        } else {
            // Return root level items
            return this.getRootIssues();
        }
    }

    private async getRootIssues(): Promise<CodeFlowIssueItem[]> {
        const issues = this.dataService.getIssues();
        const counts = this.dataService.getIssueCounts();
        const toolCounts = this.dataService.getToolIssueCounts();

        const items: CodeFlowIssueItem[] = [];

        // Add summary items
        if (counts.errors > 0) {
            items.push(new CodeFlowIssueItem(
                `❌ ${counts.errors} Errors`,
                vscode.TreeItemCollapsibleState.Collapsed
            ));
        }

        if (counts.warnings > 0) {
            items.push(new CodeFlowIssueItem(
                `⚠️ ${counts.warnings} Warnings`,
                vscode.TreeItemCollapsibleState.Collapsed
            ));
        }

        if (counts.info > 0) {
            items.push(new CodeFlowIssueItem(
                `ℹ️ ${counts.info} Info`,
                vscode.TreeItemCollapsibleState.Collapsed
            ));
        }

        // Add tool-specific groups
        Object.entries(toolCounts).forEach(([tool, count]) => {
            if (count > 0) {
                items.push(new CodeFlowIssueItem(
                    `🔧 ${tool}: ${count} issues`,
                    vscode.TreeItemCollapsibleState.Collapsed
                ));
            }
        });

        if (items.length === 0) {
            items.push(new CodeFlowIssueItem(
                '✅ No issues found',
                vscode.TreeItemCollapsibleState.None
            ));
        }

        return items;
    }

    private async getChildIssues(element: CodeFlowIssueItem): Promise<CodeFlowIssueItem[]> {
        const issues = this.dataService.getIssues();
        const label = element.label;

        if (label.includes('Errors')) {
            return this.dataService.getIssuesBySeverity('error').map(issue => 
                new CodeFlowIssueItem(
                    `${issue.file}:${issue.line} - ${issue.message}`,
                    vscode.TreeItemCollapsibleState.None,
                    issue
                )
            );
        } else if (label.includes('Warnings')) {
            return this.dataService.getIssuesBySeverity('warning').map(issue => 
                new CodeFlowIssueItem(
                    `${issue.file}:${issue.line} - ${issue.message}`,
                    vscode.TreeItemCollapsibleState.None,
                    issue
                )
            );
        } else if (label.includes('Info')) {
            return this.dataService.getIssuesBySeverity('info').map(issue => 
                new CodeFlowIssueItem(
                    `${issue.file}:${issue.line} - ${issue.message}`,
                    vscode.TreeItemCollapsibleState.None,
                    issue
                )
            );
        } else if (label.includes(':')) {
            // Tool-specific issues
            const tool = label.split(':')[0].replace('🔧 ', '');
            return this.dataService.getIssuesByTool(tool).map(issue => 
                new CodeFlowIssueItem(
                    `${issue.file}:${issue.line} - ${issue.message}`,
                    vscode.TreeItemCollapsibleState.None,
                    issue
                )
            );
        }

        return [];
    }

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }
}

export class CodeFlowMetricsProvider implements vscode.TreeDataProvider<CodeFlowMetricsItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<CodeFlowMetricsItem | undefined | null | void> = new vscode.EventEmitter<CodeFlowMetricsItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<CodeFlowMetricsItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private dataService: DataService;

    constructor() {
        this.dataService = DataService.getInstance();
    }

    getTreeItem(element: CodeFlowMetricsItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: CodeFlowMetricsItem): Promise<CodeFlowMetricsItem[]> {
        const metrics = this.dataService.getMetrics();
        const performanceHistory = this.dataService.getPerformanceHistory();

        if (!metrics) {
            return Promise.resolve([
                new CodeFlowMetricsItem('No metrics available', vscode.TreeItemCollapsibleState.None)
            ]);
        }

        const items: CodeFlowMetricsItem[] = [
            new CodeFlowMetricsItem('Code Quality Score', vscode.TreeItemCollapsibleState.None, metrics.code_quality_score, '/100'),
            new CodeFlowMetricsItem('Issues Fixed', vscode.TreeItemCollapsibleState.None, metrics.issues_fixed),
            new CodeFlowMetricsItem('Files Analyzed', vscode.TreeItemCollapsibleState.None, metrics.files_analyzed),
            new CodeFlowMetricsItem('Average Performance', vscode.TreeItemCollapsibleState.None, metrics.performance_avg, 'ms'),
            new CodeFlowMetricsItem('Complexity Score', vscode.TreeItemCollapsibleState.None, metrics.complexity_score, '/10'),
            new CodeFlowMetricsItem('Documentation Coverage', vscode.TreeItemCollapsibleState.None, metrics.documentation_coverage, '%'),
            new CodeFlowMetricsItem('Security Score', vscode.TreeItemCollapsibleState.None, metrics.security_score, '/100')
        ];

        // Add performance averages for different operations
        const operations = ['quality_check', 'auto_fix', 'file_split_analysis', 'security_scan'];
        operations.forEach(operation => {
            const avg = this.dataService.getAveragePerformance(operation);
            if (avg > 0) {
                items.push(new CodeFlowMetricsItem(
                    `${operation.replace('_', ' ').toUpperCase()} Avg`,
                    vscode.TreeItemCollapsibleState.None,
                    Math.round(avg),
                    'ms'
                ));
            }
        });

        return Promise.resolve(items);
    }

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }
}

export class CodeFlowHistoryProvider implements vscode.TreeDataProvider<CodeFlowHistoryItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<CodeFlowHistoryItem | undefined | null | void> = new vscode.EventEmitter<CodeFlowHistoryItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<CodeFlowHistoryItem | undefined | null | void> = this._onDidChangeTreeData.event;

    private dataService: DataService;

    constructor() {
        this.dataService = DataService.getInstance();
    }

    getTreeItem(element: CodeFlowHistoryItem): vscode.TreeItem {
        return element;
    }

    getChildren(element?: CodeFlowHistoryItem): Promise<CodeFlowHistoryItem[]> {
        const recentActivity = this.dataService.getRecentActivity(20);
        const learningMemory = this.dataService.getLearningMemory();

        if (recentActivity.length === 0) {
            return Promise.resolve([
                new CodeFlowHistoryItem('No recent activity', vscode.TreeItemCollapsibleState.None)
            ]);
        }

        const items: CodeFlowHistoryItem[] = [];

        // Add recent activity
        recentActivity.forEach(record => {
            const date = new Date(record.timestamp).toLocaleDateString();
            const time = new Date(record.timestamp).toLocaleTimeString();
            const label = `${date} ${time}: ${record.operation.replace('_', ' ')}`;
            
            items.push(new CodeFlowHistoryItem(
                label,
                vscode.TreeItemCollapsibleState.None,
                record
            ));
        });

        // Add learning memory patterns
        learningMemory.patterns.forEach(pattern => {
            const date = new Date(pattern.last_used).toLocaleDateString();
            const successRate = Math.round(pattern.success_rate * 100);
            const label = `${date}: ${pattern.type.replace('_', ' ')} (${successRate}% success)`;
            
            items.push(new CodeFlowHistoryItem(
                label,
                vscode.TreeItemCollapsibleState.None
            ));
        });

        return Promise.resolve(items);
    }

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }
}
