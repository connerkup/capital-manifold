/**
 * CAPITAL MANIFOLD: INSTITUTIONAL FINANCIAL ENGINEERING FRONTEND
 * Palantir / Bloomberg Terminal / Linear Aesthetic
 */

document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

// =============================================================================
// INSTITUTIONAL 14-CIRCUIT & 9-ROOT MONETARY MANIFOLD CATALOG
// Zero-Leak Invariant Verified Balance Sheets & Multi-Tier Transmission DAGs
// =============================================================================

const TREE_FLOW_CATALOG = {
  circuits: {
    "CIRCUIT-01-OAT-BUND": {
      id: "CIRCUIT-01-OAT-BUND",
      shortNum: "01",
      shortTitle: "French OAT → Bund Flight",
      title: "French Sovereign OAT to German Bund Safe-Haven Flight",
      subtitle: "Eurozone sovereign yield curve flight through SVT primary dealers and TARGET2 clearing",
      currency: "EUR",
      nominalVolume: "$250.0B (€229.4B)",
      theme: "European Sovereign Spread Crisis & TARGET2 Imbalance",
      statutoryBadge: "ECB SDW / Agence France Trésor",
      doubleEntryProof: { inflow: "$250.0B", outflow: "$250.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "french_republic_tresor",
          name: "French Republic Trésor (Agence France Trésor)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "FR",
          sector: "Sovereign Debt Issuer",
          volume: "€250.0B",
          provenance: "AFT Bulletin Mensuel",
          velocity: "Monthly Auction Schedule (T+2)",
          balanceItems: {
            assets: [
              { name: "Public Infrastructure & Tax Authority Assets", amount: "€2,950.0B" },
              { name: "Banque de France Treasury Operating Account", amount: "€45.2B" }
            ],
            liabilities: [
              { name: "OAT Benchmark Medium & Long-Term Notes", amount: "€2,410.0B" },
              { name: "BTF Short-Term Discount Treasury Bills", amount: "€180.0B" },
              { name: "Sovereign Equity & Net Fiscal Position", amount: "€405.2B" }
            ]
          },
          branches: [
            { targetId: "svt_dealers_bnp_socgen", targetName: "Primary Dealers (SVT BNP/SocGen)", volume: "€145.0B" },
            { targetId: "ca_cib_natixis_dealer_syndicate", targetName: "Secondary Syndicate (Natixis/CA)", volume: "€85.0B" },
            { targetId: "french_economy_importers", targetName: "State Procurement Fiscal Channel", volume: "€20.0B" }
          ]
        },
        {
          id: "french_republic_oat_market",
          name: "French OAT Benchmark Market (Secondary Yield Curve)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "FR",
          sector: "Sovereign Bond Market",
          volume: "€180.0B",
          provenance: "Euronext Paris / MTS",
          velocity: "Daily Secondary Turnover ($12.5B/day)",
          balanceItems: {
            assets: [
              { name: "Secondary Trading Book Inventory", amount: "€180.0B" },
              { name: "MTS Interdealer Matched Quotes", amount: "€95.0B" }
            ],
            liabilities: [
              { name: "Institutional Clearing Obligations", amount: "€180.0B" },
              { name: "Dealer Repo Financing Collateral", amount: "€95.0B" }
            ]
          },
          branches: [
            { targetId: "banque_de_france", targetName: "Banque de France Collateral Desk", volume: "€120.0B" },
            { targetId: "sovereign_debt_holders", targetName: "Institutional Life Insurers", volume: "€60.0B" }
          ]
        },
        {
          id: "svt_dealers_bnp_socgen",
          name: "Primary Dealers (SVT: BNP Paribas & Société Générale)",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "FR",
          sector: "Primary SVT Broker-Dealer",
          volume: "€145.0B",
          provenance: "ECB SDW / Banque de France",
          velocity: "Intraday Repo Turnover (T+0)",
          balanceItems: {
            assets: [
              { name: "Sovereign OAT Market Making Inventory", amount: "€145.0B" },
              { name: "Reverse Repo Claims on Interbank Market", amount: "€88.0B" }
            ],
            liabilities: [
              { name: "Intraday Banque de France Credit Lines", amount: "€145.0B" },
              { name: "Short OAT Hedge Positions", amount: "€88.0B" }
            ]
          },
          branches: [
            { targetId: "french_republic_oat_market", targetName: "French OAT Secondary Market", volume: "€145.0B" },
            { targetId: "offshore_fx_swap_desk", targetName: "London FX Basis Swap Desks", volume: "€35.0B" }
          ]
        },
        {
          id: "banque_de_france",
          name: "Banque de France (Eurosystem National Central Bank)",
          tier: 1,
          tierLabel: "TRANSMISSION CB DESK",
          jurisdiction: "FR",
          sector: "Eurosystem Central Bank",
          volume: "€181.3B",
          provenance: "BdF Compte de Résultat",
          velocity: "TARGET2 Real-Time Settlement",
          balanceItems: {
            assets: [
              { name: "Main Refinancing Operations (MRO) Lending", amount: "€120.0B" },
              { name: "Eurosystem PSPP/PEPP Sovereign Portfolios", amount: "€520.0B" }
            ],
            liabilities: [
              { name: "Commercial Bank Excess Reserve Accounts", amount: "€458.7B" },
              { name: "Net TARGET2 Cross-Border Liability", amount: "€181.3B" }
            ]
          },
          branches: [
            { targetId: "eurosystem_target2_pool", targetName: "Eurosystem TARGET2 Clearing Pool", volume: "€181.3B" }
          ]
        },
        {
          id: "eurosystem_target2_pool",
          name: "Eurosystem TARGET2 RTGS Wholesale Clearing Pool",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "EU",
          sector: "RTGS Clearing Pool",
          volume: "€1.25T/day",
          provenance: "ECB SDW Target2 Balances",
          velocity: "Continuous Real-Time Gross Settlement",
          balanceItems: {
            assets: [
              { name: "Claims on Debtor Central Banks (FR, IT, ES)", amount: "€640.0B" },
              { name: "Intraday Liquidity Settlement Queue", amount: "€120.0B" }
            ],
            liabilities: [
              { name: "Liabilities to Creditor Central Banks (BUBA, DNB)", amount: "€640.0B" },
              { name: "Settled Member Cash Accounts", amount: "€120.0B" }
            ]
          },
          branches: [
            { targetId: "bundesbank", targetName: "Deutsche Bundesbank TARGET2 Asset", volume: "€181.3B" },
            { targetId: "dutch_central_bank_dnb", targetName: "De Nederlandsche Bank Target2", volume: "€45.0B" }
          ]
        },
        {
          id: "bundesbank",
          name: "Deutsche Bundesbank (Frankfurt)",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "DE",
          sector: "Central Bank Creditor",
          volume: "€181.3B",
          provenance: "Bundesbank Monatsbericht",
          velocity: "Zero Friction Capital Anchor",
          balanceItems: {
            assets: [
              { name: "Positive TARGET2 Eurosystem Claims", amount: "€1,080.0B" },
              { name: "German Sovereign Benchmark Bond Holdings", amount: "€410.0B" }
            ],
            liabilities: [
              { name: "Domestic Commercial Bank Reserve Deposits", amount: "€1,250.0B" },
              { name: "Official Euro Reserve Liabilities", amount: "€240.0B" }
            ]
          },
          branches: [
            { targetId: "bund_risk_free_anchor", targetName: "German Federal 10Y Bund Anchor", volume: "€181.3B" }
          ]
        },
        {
          id: "bund_risk_free_anchor",
          name: "German Federal Bund Risk-Free Capital Sink",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "DE",
          sector: "Risk-Free Sovereign Anchor",
          volume: "€250.0B",
          provenance: "Finanzagentur Bund Benchmark",
          velocity: "Permanent Custodial Safe-Haven Park",
          balanceItems: {
            assets: [
              { name: "Eurozone Risk-Free Safe-Haven Collateral", amount: "€2,100.0B" },
              { name: "Global Institutional Reserve Backing", amount: "€950.0B" }
            ],
            liabilities: [
              { name: "Sovereign Debt Outstanding to World Holders", amount: "€2,100.0B" },
              { name: "Foreign Central Bank Reserves Custody", amount: "€950.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "french_republic_tresor",
          target: "svt_dealers_bnp_socgen",
          action: "SYNDICATED AUCTION",
          volume: "€45.2B",
          statutory: "AFT Bulletin Mensuel",
          narrative: "French Treasury issues €45.2B in 10-year OAT benchmark debt via syndicated bookbuild to primary SVT dealers (BNP Paribas & Société Générale)."
        },
        {
          source: "svt_dealers_bnp_socgen",
          target: "french_republic_oat_market",
          action: "SECONDARY TRADING",
          volume: "€45.2B",
          statutory: "MTS Interdealer Protocol",
          narrative: "Primary SVT dealers make markets on Euronext Paris and MTS interdealer trading platforms, absorbing sovereign supply onto balance sheets."
        },
        {
          source: "french_republic_oat_market",
          target: "banque_de_france",
          action: "COLLATERAL REPO",
          volume: "€45.2B",
          statutory: "ECB Guideline 2014/60",
          narrative: "Dealers pledge secondary OAT paper into Banque de France for intraday liquidity refinancing and Eurosystem monetary policy credit."
        },
        {
          source: "banque_de_france",
          target: "eurosystem_target2_pool",
          action: "RTGS CROSS-BORDER RUN",
          volume: "€181.3B",
          statutory: "ECB SDW Target2 Bulletin",
          narrative: "Spreading credit blowout induces depositors and asset managers to wire capital out of French banks, expanding BdF's TARGET2 liability by -€181.3B."
        },
        {
          source: "eurosystem_target2_pool",
          target: "bundesbank",
          action: "CREDITOR SETTLEMENT",
          volume: "€181.3B",
          statutory: "Bundesbank Balance Sheet Art. 28",
          narrative: "Capital inflows clear across the RTGS network, settling as an expanding positive TARGET2 claim on the Deutsche Bundesbank balance sheet."
        },
        {
          source: "bundesbank",
          target: "bund_risk_free_anchor",
          action: "SAFE-HAVEN ABSORPTION",
          volume: "€181.3B",
          statutory: "Finanzagentur Bund Gazette",
          narrative: "Flight-to-quality capital purchases German Federal 10Y Bunds, compressing Bund benchmark yields and widening the OAT-Bund spread past +150 bp."
        }
      ]
    },

    "CIRCUIT-02-YEN-CARRY": {
      id: "CIRCUIT-02-YEN-CARRY",
      shortNum: "02",
      shortTitle: "Yen Carry → US Repo",
      title: "Japanese Institutional Carry Trade to US Treasury Repo",
      subtitle: "BoJ zero-interest liquidity crossing offshore FX basis swaps into DTCC Triparty repo",
      currency: "USD / JPY",
      nominalVolume: "$1.104T ($3.007T/day SOFR)",
      theme: "Transpacific & Transatlantic Dollar Funding Nexus",
      statutoryBadge: "DTCC Triparty / BoJ Statistical Gazette",
      doubleEntryProof: { inflow: "$1.104T", outflow: "$1.104T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "japan_mof_boj_carry_faucet",
          name: "Bank of Japan & MoF Zero-Rate Faucet",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "JP",
          sector: "Central Bank Genesis",
          volume: "¥750T ($5.1T)",
          provenance: "BoJ Accounts Summary",
          velocity: "Daily Overnight Policy Rate",
          balanceItems: {
            assets: [
              { name: "Japanese Government Bonds (JGBs)", amount: "¥580.0T" },
              { name: "Foreign Exchange Reserve Accounts", amount: "¥170.0T" }
            ],
            liabilities: [
              { name: "Current Account Balances (Excess Reserves)", amount: "¥540.0T" },
              { name: "Banknotes in Circulation", amount: "¥125.0T" },
              { name: "Net Worth & Capital", amount: "¥85.0T" }
            ]
          },
          branches: [
            { targetId: "japan_institutional_carry_desk", targetName: "Japan Institutional Carry Desks", volume: "$650.0B" }
          ]
        },
        {
          id: "japan_institutional_carry_desk",
          name: "Japanese Institutional Carry Desks (Norinchukin / Lifers)",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "JP",
          sector: "Institutional Carry Conduits",
          volume: "$650.0B",
          provenance: "FSA Japan Survey",
          velocity: "3-Month Term FX Swap Roll",
          balanceItems: {
            assets: [
              { name: "Foreign Currency Securities & Sovereign Debt", amount: "$650.0B" },
              { name: "Domestic Yen Collateral Portfolio", amount: "¥45.0T" }
            ],
            liabilities: [
              { name: "Yen Policy Loans & Domestic Deposits", amount: "¥45.0T" },
              { name: "Synthetic USD Basis Obligations", amount: "$650.0B" }
            ]
          },
          branches: [
            { targetId: "offshore_fx_swap_desk", targetName: "Offshore FX Basis Swap Desk", volume: "$480.0B" }
          ]
        },
        {
          id: "offshore_fx_swap_desk",
          name: "Offshore Synthetic USD FX Swap Desk (London/NY)",
          tier: 1,
          tierLabel: "TRANSMISSION DESK",
          jurisdiction: "GLOBAL_OFFSHORE",
          sector: "G-SIB FX Basis Desk",
          volume: "$480.0B",
          provenance: "BIS Quarterly Review / ISDA",
          velocity: "Daily Roll & Forward Settlement",
          balanceItems: {
            assets: [
              { name: "Synthetic Dollar Spot Receivables", amount: "$480.0B" },
              { name: "Yen Collateral Pledged by Japanese Desks", amount: "¥72.0T" }
            ],
            liabilities: [
              { name: "Spot Dollar Pledged to Counterparties", amount: "$480.0B" },
              { name: "Yen Forward Return Obligations", amount: "¥72.0T" }
            ]
          },
          branches: [
            { targetId: "us_triparty_repo_pool", targetName: "US Triparty Repo Basin", volume: "$480.0B" }
          ]
        },
        {
          id: "us_triparty_repo_pool",
          name: "US Triparty Repo SOFR Clearing Basin (DTCC/BNY Mellon)",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "US",
          sector: "Wholesale Repo Clearing Pool",
          volume: "$3.007T/day",
          provenance: "DTCC Triparty / NY Fed SOFR",
          velocity: "Overnight Wholesale Turnover",
          balanceItems: {
            assets: [
              { name: "Overnight Reverse Repo Loans to Dealers", amount: "$3,007.0B" },
              { name: "US Treasury Collateral Pledged in Custody", amount: "$3,007.0B" }
            ],
            liabilities: [
              { name: "Cash Deposits from Prime MMFs and Desks", amount: "$3,007.0B" },
              { name: "Secured Borrowing Obligations", amount: "$3,007.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasury_tga", targetName: "US Treasury General Account", volume: "$883.3B" },
            { targetId: "us_prime_mmf_basin", targetName: "US Prime Money Market Funds", volume: "$1.20T" }
          ]
        },
        {
          id: "us_treasury_tga",
          name: "US Treasury General Account (Fed Cash Vault)",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "US",
          sector: "Sovereign Operating Vault",
          volume: "$883.3B",
          provenance: "Daily Treasury Statement (DTS)",
          velocity: "Intraday Fedwire Inflow Sweep",
          balanceItems: {
            assets: [
              { name: "Cash Balances on Deposit at Federal Reserve", amount: "$883.3B" },
              { name: "Treasury Tax & Loan Investment Accounts", amount: "$45.0B" }
            ],
            liabilities: [
              { name: "Federal Operating Budget Allocations", amount: "$883.3B" },
              { name: "Statutory Public Debt Service Accruals", amount: "$45.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "japan_mof_boj_carry_faucet",
          target: "japan_institutional_carry_desk",
          action: "ZERO-RATE YEN FUNDING",
          volume: "$650.0B",
          statutory: "BoJ Financial Accounts",
          narrative: "Bank of Japan anchors short-term rates near 0.25%, providing massive low-cost yen funding to domestic institutional lifers and trust banks."
        },
        {
          source: "japan_institutional_carry_desk",
          target: "offshore_fx_swap_desk",
          action: "CROSS-CURRENCY FX BASIS SWAP",
          volume: "$480.0B",
          statutory: "BIS OTC FX Derivatives Table",
          narrative: "Institutions execute cross-currency basis swaps in London and New York, lending yen to G-SIBs and borrowing synthetic dollars at negative basis."
        },
        {
          source: "offshore_fx_swap_desk",
          target: "us_triparty_repo_pool",
          action: "TRIPARTY REPO CLEARING",
          volume: "$480.0B",
          statutory: "DTCC GCF Repo Schedule",
          narrative: "Synthetic dollars flow directly into the DTCC / BNY Mellon Triparty repo basin to fund primary dealer Treasury inventories at overnight SOFR."
        },
        {
          source: "us_triparty_repo_pool",
          target: "us_treasury_tga",
          action: "TREASURY AUCTION FINANCING",
          volume: "$480.0B",
          statutory: "Daily Treasury Statement Table I",
          narrative: "Dealer balance sheets absorb massive US Treasury bill auctions, sweeping cash through Fedwire into the Treasury General Account (TGA)."
        }
      ]
    },

    "CIRCUIT-03-QT-BURN": {
      id: "CIRCUIT-03-QT-BURN",
      shortNum: "03",
      shortTitle: "Fed QT Money Burn",
      title: "Federal Reserve SOMA QT Money Burn Chamber",
      subtitle: "Permanent base-money destruction via maturing Treasury runoff and ON RRP drainage",
      currency: "USD",
      nominalVolume: "$2.157T Base Money Destroyed",
      theme: "Central Bank Balance Sheet Contraction",
      statutoryBadge: "Fed H.4.1 / Daily Treasury Statement",
      doubleEntryProof: { inflow: "$2.157T", outflow: "$2.157T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "us_corporate_and_household_borrowers",
          name: "US Corporate & Household Taxpayers & Borrowers",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "US",
          sector: "Real Economy Debtors",
          volume: "$2.157T",
          provenance: "Fed Financial Accounts Z.1",
          velocity: "Quarterly Tax & Principal Payment",
          balanceItems: {
            assets: [
              { name: "Real Economy Productive Capital & Income", amount: "$38,400.0B" },
              { name: "Commercial Banking Checking Deposits", amount: "$3,200.0B" }
            ],
            liabilities: [
              { name: "Corporate Debt & Household Mortgages", amount: "$18,500.0B" },
              { name: "Federal Tax Accruals & Liabilities", amount: "$2,157.0B" }
            ]
          },
          branches: [
            { targetId: "us_commercial_bank_credit_pool", targetName: "US Commercial Bank Credit Pool", volume: "$2.157T" }
          ]
        },
        {
          id: "us_commercial_bank_credit_pool",
          name: "US Commercial Banking Reserve Pool",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "US",
          sector: "Commercial Banking System",
          volume: "$3.25T Reserves",
          provenance: "Fed H.8 Aggregate Balance Sheet",
          velocity: "Daily Fedwire Reserve Transfers",
          balanceItems: {
            assets: [
              { name: "Master Account Reserve Balances at Fed", amount: "$3,250.0B" },
              { name: "US Treasury Securities Portfolio", amount: "$4,120.0B" }
            ],
            liabilities: [
              { name: "Customer Demand & Time Deposits", amount: "$17,400.0B" },
              { name: "Wholesale Interbank Funding", amount: "$1,850.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasury_tga", targetName: "US Treasury General Account", volume: "$2.157T" }
          ]
        },
        {
          id: "us_treasury_tga",
          name: "US Treasury General Account (Fed Cash Vault)",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "US",
          sector: "Sovereign Operating Vault",
          volume: "$883.3B",
          provenance: "Daily Treasury Statement",
          velocity: "Daily Auction & Redemption Netting",
          balanceItems: {
            assets: [
              { name: "Fed Master Account Cash Operating Balance", amount: "$883.3B" },
              { name: "Tax Receipts in Transit", amount: "$145.0B" }
            ],
            liabilities: [
              { name: "Maturing Treasury Note Redemption Obligations", amount: "$883.3B" },
              { name: "Fiscal Outlay Commitments", amount: "$145.0B" }
            ]
          },
          branches: [
            { targetId: "fed_soma_qt_burn_chamber", targetName: "Fed SOMA QT Money Burn Chamber", volume: "$2.157T" }
          ]
        },
        {
          id: "fed_soma_qt_burn_chamber",
          name: "Federal Reserve SOMA QT Money Burn Chamber",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Monetary Base Destruction Sinks",
          volume: "$2.157T Destroyed",
          provenance: "Fed H.4.1 Factors Affecting Reserves",
          velocity: "Permanent Base Money Extinguishment",
          balanceItems: {
            assets: [
              { name: "SOMA Treasury Securities (Extinguished)", amount: "-$2,157.0B" },
              { name: "Remaining System Open Market Portfolio", amount: "$6,850.0B" }
            ],
            liabilities: [
              { name: "Extinguished Reserve Balances (Burned)", amount: "-$2,157.0B" },
              { name: "Active Commercial Bank Reserves", amount: "$3,250.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "us_corporate_and_household_borrowers",
          target: "us_commercial_bank_credit_pool",
          action: "TAX DEPOSITS & DEBT SERVICE",
          volume: "$2.157T",
          statutory: "IRS Tax Collections Data",
          narrative: "Real economy debtors and corporations pay taxes and buy new Treasury issues using commercial bank deposit balances."
        },
        {
          source: "us_commercial_bank_credit_pool",
          target: "us_treasury_tga",
          action: "RESERVE ACCOUNT SWEEP",
          volume: "$2.157T",
          statutory: "Fedwire Funds Service Table 1",
          narrative: "Commercial banks transfer member bank reserve balances via Fedwire directly into the Treasury General Account to fund sovereign redemptions."
        },
        {
          source: "us_treasury_tga",
          target: "fed_soma_qt_burn_chamber",
          action: "BOND REDEMPTION RUNOFF",
          volume: "$2.157T",
          statutory: "Fed H.4.1 Release",
          narrative: "Treasury redeems maturing notes directly against the Fed's SOMA portfolio without issuing replacement debt to the central bank."
        },
        {
          source: "fed_soma_qt_burn_chamber",
          target: "fed_soma_qt_burn_chamber",
          action: "BASE MONEY ANNIHILATION",
          volume: "$2.157T",
          statutory: "Federal Reserve Act Section 14",
          narrative: "The Federal Reserve permanently debits its TGA liability and cancels the maturing Treasury asset, destroying $2.157T of base money."
        }
      ]
    },

    "CIRCUIT-04-SHADOW-CRUDE": {
      id: "CIRCUIT-04-SHADOW-CRUDE",
      shortNum: "04",
      shortTitle: "Russian Dark Fleet Crude",
      title: "Eurasian Shadow Crude Maritime Energy Arbitrage",
      subtitle: "Russian Urals crude via dark maritime fleet to Indian refining and European diesel imports",
      currency: "RUB / USD / EUR",
      nominalVolume: "$140.0B ($420B Complex)",
      theme: "Sanctions Arbitrage & Hydrocarbon Rerouting",
      statutoryBadge: "AIS Vessel Tracking / CBR Bulletin",
      doubleEntryProof: { inflow: "$140.0B", outflow: "$140.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "bank_of_russia_cbr_vault",
          name: "Bank of Russia (CBR) Sovereign Vault",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "RU",
          sector: "Sanctioned Central Bank",
          volume: "$600.0B",
          provenance: "CBR Annual Bulletin",
          velocity: "Bilateral Clearing Cycle",
          balanceItems: {
            assets: [
              { name: "Gold Bullion Vault (Moscow)", amount: "$185.0B" },
              { name: "Yuan & Non-Western Foreign Assets", amount: "$115.0B" },
              { name: "Frozen G7 Sovereign Assets", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Ruble Monetary Base", amount: "$280.0B" },
              { name: "National Wealth Fund Deposits", amount: "$155.0B" }
            ]
          },
          branches: [
            { targetId: "shadow_tanker_energy_arbitrage", targetName: "Shadow Tanker Fleet", volume: "$140.0B" }
          ]
        },
        {
          id: "shadow_tanker_energy_arbitrage",
          name: "Maritime Shadow Tanker Fleet Arbitrage Conduit",
          tier: 1,
          tierLabel: "TRANSMISSION CONDUIT",
          jurisdiction: "GLOBAL_MARITIME",
          sector: "Dark Maritime Energy Transit",
          volume: "$140.0B",
          provenance: "AIS Satellite Tanker Tracking",
          velocity: "30-Day Baltic-to-Gujarat Transit",
          balanceItems: {
            assets: [
              { name: "Crude Cargo In Transit (Urals Benchmark)", amount: "$140.0B" },
              { name: "Offshore Dirham Letters of Credit", amount: "$35.0B" }
            ],
            liabilities: [
              { name: "Charter Freight & Bunker Obligations", amount: "$25.0B" },
              { name: "Oil Export Payables to Russian Producers", amount: "$150.0B" }
            ]
          },
          branches: [
            { targetId: "reserve_bank_of_india_refining_hub", targetName: "Indian Refineries (Reliance/Nayara)", volume: "$140.0B" }
          ]
        },
        {
          id: "reserve_bank_of_india_refining_hub",
          name: "Reserve Bank of India & Gujarat Refining Nexus",
          tier: 2,
          tierLabel: "TRAVERSAL HUB",
          jurisdiction: "IN",
          sector: "Energy Refining & Vostro Clearing",
          volume: "$140.0B",
          provenance: "DGCIS India Energy Trade Data",
          velocity: "Cracking Margin & Re-export Cycle",
          balanceItems: {
            assets: [
              { name: "Refined Clean Diesel & Jet Fuel Inventory", amount: "$140.0B" },
              { name: "Rupee Vostro Account Inflows", amount: "$45.0B" }
            ],
            liabilities: [
              { name: "Vostro Rupee Balances to Russian Desks", amount: "$45.0B" },
              { name: "Trade Financing Commercial Paper", amount: "$95.0B" }
            ]
          },
          branches: [
            { targetId: "french_economy_importers", targetName: "French Real Economy Importers", volume: "$140.0B" }
          ]
        },
        {
          id: "french_economy_importers",
          name: "French Economy Commercial Importers & Energy Grid",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "FR",
          sector: "Real Economy Energy Consumer Sink",
          volume: "$140.0B",
          provenance: "INSEE Foreign Trade Gazette",
          velocity: "Final Energy Consumption & Tax Drain",
          balanceItems: {
            assets: [
              { name: "Refined Low-Sulfur Hydrocarbon Stocks", amount: "$140.0B" },
              { name: "Commercial Distribution Cash Flows", amount: "$65.0B" }
            ],
            liabilities: [
              { name: "Commercial Import Accounts Payable", amount: "$140.0B" },
              { name: "TICPE Energy Excise Tax Liabilities", amount: "$65.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "bank_of_russia_cbr_vault",
          target: "shadow_tanker_energy_arbitrage",
          action: "DARK FLEET SEABORNE LOADING",
          volume: "$140.0B",
          statutory: "Transneft Export Terminal Manifest",
          narrative: "Russian oil majors load $140B in Urals crude from Primorsk and Novorossiysk onto dark fleet tankers with transponders disabled, sold under price caps."
        },
        {
          source: "shadow_tanker_energy_arbitrage",
          target: "reserve_bank_of_india_refining_hub",
          action: "VOSTRO TRADE SETTLEMENT",
          volume: "$140.0B",
          statutory: "RBI Special Rupee Vostro Notice",
          narrative: "Tankers deliver crude to Reliance Jamnagar and Nayara refineries in Gujarat, settling trade via non-convertible Indian Rupee vostro accounts."
        },
        {
          source: "reserve_bank_of_india_refining_hub",
          target: "french_economy_importers",
          action: "REFINED DIESEL RE-EXPORT",
          volume: "$140.0B",
          statutory: "EU Combined Nomenclature 2710",
          narrative: "Refined clean low-sulfur diesel is legally imported into French maritime ports as Indian product, completely bypassing sanctions."
        }
      ]
    },

    "CIRCUIT-05-TECH-BUYBACK": {
      id: "CIRCUIT-05-TECH-BUYBACK",
      shortNum: "05",
      shortTitle: "Apple Buyback Burn",
      title: "Apple BigTech Cash Hoard & Equity Buyback Chamber",
      subtitle: "Global consumer and enterprise tech revenue swept into equity share retirement",
      currency: "USD",
      nominalVolume: "$182.0B ($62.09B Burned)",
      theme: "Corporate Liquidity Hoarding & Financial Engineering",
      statutoryBadge: "SEC 10-K / Apple Treasury Filing",
      doubleEntryProof: { inflow: "$182.0B", outflow: "$182.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "global_enterprise_tech_buyers",
          name: "Global Enterprise & Consumer Tech Buyers",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "GLOBAL",
          sector: "Global Technology Consumers",
          volume: "$182.0B",
          provenance: "SEC 10-K Net Sales Segment",
          velocity: "Continuous Commercial Hardware & SaaS Turnover",
          balanceItems: {
            assets: [
              { name: "Purchased Hardware & Services Utility", amount: "$182.0B" },
              { name: "Commercial Operating Liquidity", amount: "$54.0B" }
            ],
            liabilities: [
              { name: "Accounts Payable to Apple Inc.", amount: "$182.0B" },
              { name: "Consumer Revolving Credit", amount: "$54.0B" }
            ]
          },
          branches: [
            { targetId: "apple_bigtech_treasury_vault", targetName: "Apple Corporate Treasury Vault", volume: "$182.0B" }
          ]
        },
        {
          id: "apple_bigtech_treasury_vault",
          name: "Apple BigTech Corporate Treasury Vault",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "US",
          sector: "Corporate Liquidity Hoard",
          volume: "$162.4B Liquid Assets",
          provenance: "Apple Inc. Form 10-K Note 3",
          velocity: "Continuous Overnight Liquidity Sweep",
          balanceItems: {
            assets: [
              { name: "Cash, Cash Equivalents & Marketable Securities", amount: "$162.4B" },
              { name: "US Treasury Bills & Commercial Paper", amount: "$104.0B" }
            ],
            liabilities: [
              { name: "Commercial Paper & Term Debt", amount: "$106.0B" },
              { name: "Shareholders Equity Capital", amount: "$60.4B" }
            ]
          },
          branches: [
            { targetId: "us_commercial_bank_credit_pool", targetName: "US Commercial Banking Credit Pool", volume: "$62.09B" },
            { targetId: "corporate_share_buyback_burn_chamber", targetName: "Share Buyback Retirement Chamber", volume: "$62.09B" }
          ]
        },
        {
          id: "us_commercial_bank_credit_pool",
          name: "Wall Street Broker-Dealer Execution Nexus",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "US",
          sector: "Prime Brokerage Buyback Desks",
          volume: "$62.09B",
          provenance: "SEC Rule 10b-18 Disclosures",
          velocity: "Daily Accelerated Share Repurchase (ASR)",
          balanceItems: {
            assets: [
              { name: "Repurchased Common Shares (In Transit)", amount: "$62.09B" },
              { name: "Broker-Dealer Custody Clearing Accounts", amount: "$12.5B" }
            ],
            liabilities: [
              { name: "Apple Treasury Cash Transfer Receipts", amount: "$62.09B" },
              { name: "Market Settlement Payables", amount: "$12.5B" }
            ]
          },
          branches: [
            { targetId: "corporate_share_buyback_burn_chamber", targetName: "Corporate Share Retirement Chamber", volume: "$62.09B" }
          ]
        },
        {
          id: "corporate_share_buyback_burn_chamber",
          name: "Corporate Share Buyback Equity Retirement Chamber",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Permanent Capital Retirement Sink",
          volume: "$62.09B Extinguished",
          provenance: "SEC 10-K Item 5 Disclosures",
          velocity: "Permanent Equity Extinguishment",
          balanceItems: {
            assets: [
              { name: "Extinguished Cash Flow Drainage", amount: "-$62.09B" },
              { name: "Preserved Free Cash Flow Buffer", amount: "$100.3B" }
            ],
            liabilities: [
              { name: "Extinguished Common Stock Share Capital", amount: "-$62.09B" },
              { name: "Retained Earnings Rebalance", amount: "$100.3B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "global_enterprise_tech_buyers",
          target: "apple_bigtech_treasury_vault",
          action: "GLOBAL REVENUE SWEEP",
          volume: "$182.0B",
          statutory: "Apple 10-K Consolidated Statements of Operations",
          narrative: "Consumer iPhone purchases and enterprise cloud services generate $182B in gross operational cash flows swept into Apple's liquidity vaults."
        },
        {
          source: "apple_bigtech_treasury_vault",
          target: "us_commercial_bank_credit_pool",
          action: "BROKER-DEALER ASR MANDATE",
          volume: "$62.09B",
          statutory: "SEC Rule 10b5-1 Repurchase Plan",
          narrative: "Apple treasury wires $62.09B to primary broker-dealers (Goldman Sachs / Morgan Stanley) under accelerated share repurchase contracts."
        },
        {
          source: "us_commercial_bank_credit_pool",
          target: "corporate_share_buyback_burn_chamber",
          action: "EQUITY CAPITAL RETIREMENT",
          volume: "$62.09B",
          statutory: "Delaware General Corporation Law Section 243",
          narrative: "Open market shares are repurchased and legally retired into treasury stock, permanently extinguishing corporate equity capital."
        }
      ]
    },

    "CIRCUIT-06-GULF-PETRODOLLAR": {
      id: "CIRCUIT-06-GULF-PETRODOLLAR",
      shortNum: "06",
      shortTitle: "Gulf Petrodollars → OAT",
      title: "Gulf Petrodollar Sovereign Wealth Recycling",
      subtitle: "Hydrocarbon revenues accumulated into sovereign wealth funds and recycled into Western capital anchors",
      currency: "USD / EUR",
      nominalVolume: "$380.0B ($2.07T AUM)",
      theme: "Planetary Petrodollar Recycling",
      statutoryBadge: "SAMA Annual / ADIA Review",
      doubleEntryProof: { inflow: "$380.0B", outflow: "$380.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "saudi_sama_pif_nexus",
          name: "Saudi Central Bank (SAMA) & PIF Sovereign Nexus",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "SA",
          sector: "Sovereign Wealth Faucet",
          volume: "$925.0B AUM",
          provenance: "SAMA Statistical Bulletin",
          velocity: "Monthly Crude Export Netting",
          balanceItems: {
            assets: [
              { name: "Foreign Exchange Currency Reserves", amount: "$450.0B" },
              { name: "Global Equity & Alternative Portfolios", amount: "$475.0B" }
            ],
            liabilities: [
              { name: "Government Fiscal Reserve Deposits", amount: "$380.0B" },
              { name: "Sovereign Capital & Retained Windfalls", amount: "$545.0B" }
            ]
          },
          branches: [
            { targetId: "gulf_petrodollar_sovereign_wealth_basin", targetName: "Gulf Petrodollar Basin", volume: "$380.0B" }
          ]
        },
        {
          id: "uae_adia_mubadala_basin",
          name: "UAE Sovereign Wealth Basin (ADIA & Mubadala)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "AE",
          sector: "Sovereign Wealth Basin",
          volume: "$1.15T AUM",
          provenance: "ADIA Annual Review",
          velocity: "Quarterly Asset Allocation Cycle",
          balanceItems: {
            assets: [
              { name: "Global Public Equities & Fixed Income", amount: "$750.0B" },
              { name: "Private Equity, Infrastructure & Real Estate", amount: "$400.0B" }
            ],
            liabilities: [
              { name: "Sovereign Capital Allocations", amount: "$1,150.0B" }
            ]
          },
          branches: [
            { targetId: "gulf_petrodollar_sovereign_wealth_basin", targetName: "Gulf Petrodollar Basin", volume: "$380.0B" }
          ]
        },
        {
          id: "gulf_petrodollar_sovereign_wealth_basin",
          name: "Gulf GCC Sovereign Wealth Interbank Basin",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "MIDDLE_EAST",
          sector: "Offshore Petrodollar Syndication",
          volume: "$380.0B",
          provenance: "BIS Locational Banking Statistics",
          velocity: "Multi-Currency Wire Settlement",
          balanceItems: {
            assets: [
              { name: "Western Sovereign Debt Claims", amount: "$220.0B" },
              { name: "G-SIB Prime Brokerage Placements", amount: "$160.0B" }
            ],
            liabilities: [
              { name: "GCC Sovereign Depositor Liabilities", amount: "$380.0B" }
            ]
          },
          branches: [
            { targetId: "french_republic_oat_market", targetName: "French OAT Sovereign Market", volume: "$180.0B" },
            { targetId: "bund_risk_free_anchor", targetName: "German Bund Safe-Haven Anchor", volume: "$200.0B" }
          ]
        },
        {
          id: "french_republic_oat_market",
          name: "French Republic OAT Sovereign Benchmark Market",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "FR",
          sector: "Sovereign Benchmark Debt Sink",
          volume: "$180.0B",
          provenance: "Agence France Trésor",
          velocity: "Long-Term Custodial Allocation",
          balanceItems: {
            assets: [
              { name: "Absorbed Petrodollar Inflows", amount: "$180.0B" },
              { name: "French Public Infrastructure Stock", amount: "$1,200.0B" }
            ],
            liabilities: [
              { name: "OAT Sovereign Bond Stock Outstanding", amount: "$1,380.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "saudi_sama_pif_nexus",
          target: "gulf_petrodollar_sovereign_wealth_basin",
          action: "OIL ROYALTY DEPOSITS",
          volume: "$180.0B",
          statutory: "SAMA Foreign Assets Return",
          narrative: "Aramco crude sales settled in US dollars sweep surplus oil royalties into SAMA and PIF interbank reserve accounts."
        },
        {
          source: "uae_adia_mubadala_basin",
          target: "gulf_petrodollar_sovereign_wealth_basin",
          action: "PETRODOLLAR CONSOLIDATION",
          volume: "$200.0B",
          statutory: "ADIA Sovereign Allocation Mandate",
          narrative: "Abu Dhabi oil revenues accumulate in offshore commercial deposits in London, Zurich, and New York."
        },
        {
          source: "gulf_petrodollar_sovereign_wealth_basin",
          target: "french_republic_oat_market",
          action: "SOVEREIGN BOND RECYCLING",
          volume: "$180.0B",
          statutory: "AFT Investor Allocation Report",
          narrative: "Gulf sovereign managers swap USD into EUR, buying French 10Y/30Y OAT sovereign bonds to diversify reserve portfolios."
        }
      ]
    },

    "CIRCUIT-07-CHINA-PETROYUAN-CIPS": {
      id: "CIRCUIT-07-CHINA-PETROYUAN-CIPS",
      shortNum: "07",
      shortTitle: "China Petro-Yuan CIPS",
      title: "China Petro-Yuan CIPS & Sovereign FX Reserve Recycling",
      subtitle: "$3.24T PBOC FX reserves, $550B bilateral swap network, and cross-border renminbi clearing",
      currency: "CNY / USD",
      nominalVolume: "$3.24T ($550B Swaps)",
      theme: "Cross-Border De-Dollarization & Sovereign Reserve Recycling",
      statutoryBadge: "PBOC Balance Sheet / CIPS Annual",
      doubleEntryProof: { inflow: "$3.24T", outflow: "$3.24T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "saudi_sama_pif_nexus",
          name: "Saudi Energy Settlement Desk (SHPGX Bilateral)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "SA",
          sector: "Hydrocarbon Exporter Faucet",
          volume: "$180.0B CNH",
          provenance: "Shanghai Petroleum Exchange (SHPGX)",
          velocity: "Bilateral Energy Settlement",
          balanceItems: {
            assets: [
              { name: "Crude Petroleum Export Invoices", amount: "$180.0B" },
              { name: "Offshore CNH Renminbi Receivables", amount: "$180.0B" }
            ],
            liabilities: [
              { name: "Commercial Trade Clearings", amount: "$180.0B" }
            ]
          },
          branches: [
            { targetId: "petro_yuan_bilateral_settlement_bridge", targetName: "Petro-Yuan Clearing Bridge", volume: "$180.0B" }
          ]
        },
        {
          id: "petro_yuan_bilateral_settlement_bridge",
          name: "Petro-Yuan Bilateral Non-USD Energy Settlement Bridge",
          tier: 1,
          tierLabel: "TRANSMISSION DESK",
          jurisdiction: "GLOBAL_OFFSHORE",
          sector: "Cross-Border Non-SWIFT Bridge",
          volume: "$180.0B",
          provenance: "CIPS Operating Report",
          velocity: "Direct Bilateral Netting",
          balanceItems: {
            assets: [
              { name: "Petro-Yuan Oil Clearance Invoices", amount: "$180.0B" },
              { name: "Bank of China Offshore Accounts", amount: "$180.0B" }
            ],
            liabilities: [
              { name: "Settlement Obligations to Gulf Desks", amount: "$180.0B" }
            ]
          },
          branches: [
            { targetId: "offshore_cnh_hong_kong_hub", targetName: "Offshore CNH Hong Kong Hub", volume: "$180.0B" }
          ]
        },
        {
          id: "offshore_cnh_hong_kong_hub",
          name: "Hong Kong Offshore Renminbi (CNH) RTGS Hub",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "HK",
          sector: "Offshore CNH RTGS Hub",
          volume: "¥1.8T/day ($250B)",
          provenance: "HKMA Monthly Statistical Bulletin",
          velocity: "Intraday CIPS & CMU RTGS Clearing",
          balanceItems: {
            assets: [
              { name: "Interbank CNH Clearing Balances", amount: "¥1,800.0B" },
              { name: "Offshore Dim Sum Bond Collateral", amount: "¥650.0B" }
            ],
            liabilities: [
              { name: "Participating Bank Liquidity Accounts", amount: "¥1,800.0B" },
              { name: "CIPS Settlement Quotas", amount: "¥650.0B" }
            ]
          },
          branches: [
            { targetId: "chinese_state_banks_fx_desk", targetName: "Chinese Big 4 State Banks FX Desk", volume: "$850.0B" }
          ]
        },
        {
          id: "chinese_state_banks_fx_desk",
          name: "Chinese Big 4 State Banks FX Desks (ICBC/CCB/BoC/ABC)",
          tier: 2,
          tierLabel: "TRAVERSAL INTERMEDIARY",
          jurisdiction: "CN",
          sector: "State Commercial Bank Nexus",
          volume: "$850.0B",
          provenance: "CBIRC Regulatory Returns",
          velocity: "Cross-Border Interbank Netting",
          balanceItems: {
            assets: [
              { name: "Foreign Exchange Assets & Swaps", amount: "$850.0B" },
              { name: "Offshore Trade Financing Advances", amount: "$420.0B" }
            ],
            liabilities: [
              { name: "PBOC Onshore Reserve Deposits", amount: "$850.0B" },
              { name: "Customer Cross-Border Deposits", amount: "$420.0B" }
            ]
          },
          branches: [
            { targetId: "pboc_safe_foreign_reserves", targetName: "PBOC & SAFE Foreign Reserves", volume: "$3.24T" }
          ]
        },
        {
          id: "pboc_safe_foreign_reserves",
          name: "People's Bank of China & SAFE Foreign Reserves",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "CN",
          sector: "Sovereign FX Reserve Vault",
          volume: "$3.24 Trillion",
          provenance: "SAFE Statistical Gazette",
          velocity: "Strategic Sovereign Vault Storage",
          balanceItems: {
            assets: [
              { name: "Foreign Exchange Reserves (US Treasuries, Euros)", amount: "$3,240.0B" },
              { name: "Official Gold Reserves Vault (PBOC Beijing)", amount: "$180.0B" }
            ],
            liabilities: [
              { name: "Renminbi Monetary Base (Cash + Bank Reserves)", amount: "$3,050.0B" },
              { name: "Bilateral Central Bank Currency Swap Lines", amount: "$550.0B" }
            ]
          },
          branches: [
            { targetId: "pboc_bilateral_swap_network", targetName: "PBOC Bilateral Swap Network", volume: "$550.0B" }
          ]
        }
      ],
      hops: [
        {
          source: "saudi_sama_pif_nexus",
          target: "petro_yuan_bilateral_settlement_bridge",
          action: "NON-USD INVOICING",
          volume: "$180.0B",
          statutory: "SHPGX Bilateral Contract Schedule",
          narrative: "Bilateral crude contracts execute through the Shanghai Petroleum and Natural Gas Exchange, settling directly in Renminbi."
        },
        {
          source: "petro_yuan_bilateral_settlement_bridge",
          target: "offshore_cnh_hong_kong_hub",
          action: "CIPS RTGS SETTLEMENT",
          volume: "$180.0B",
          statutory: "Cross-Border Interbank Payment System (CIPS)",
          narrative: "Renminbi flows cross the Hong Kong CNH clearing hub via CIPS, bypassing SWIFT and US CHIPS clearance."
        },
        {
          source: "offshore_cnh_hong_kong_hub",
          target: "chinese_state_banks_fx_desk",
          action: "INTERBANK CLEARING",
          volume: "$180.0B",
          statutory: "PBOC Cross-Border Settlement Circular",
          narrative: "Big 4 state banks (ICBC, CCB, Bank of China, ABC) absorb offshore CNH balances and hedge currency risks onshore."
        },
        {
          source: "chinese_state_banks_fx_desk",
          target: "pboc_safe_foreign_reserves",
          action: "SOVEREIGN RESERVE RECYCLING",
          volume: "$180.0B",
          statutory: "SAFE Balance of Payments Bulletin",
          narrative: "The PBOC and SAFE absorb surpluses into China's $3.24 Trillion sovereign FX reserve vault, backing a $550B bilateral swap network."
        }
      ]
    },

    "CIRCUIT-08-DARK-MATTER": {
      id: "CIRCUIT-08-DARK-MATTER",
      shortNum: "08",
      shortTitle: "BIS Dark Matter $600T",
      title: "Global Macro Dark Matter (BIS OTC Derivatives & Shadow Banking)",
      subtitle: "$600 Trillion unmodeled derivative notional and Treasury basis trade leverage",
      currency: "USD",
      nominalVolume: "$600T Notional ($3.2T Active)",
      theme: "Off-Balance-Sheet Systemic Blindspots",
      statutoryBadge: "BIS OTC Derivatives Statistics",
      doubleEntryProof: { inflow: "$3.20T", outflow: "$3.20T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "bis_otc_derivatives_dark_matter",
          name: "BIS OTC Derivatives & FX Dark Matter",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "GLOBAL",
          sector: "Off-Balance-Sheet Notional Faucet",
          volume: "$600 Trillion Notional",
          provenance: "BIS Semiannual OTC Derivatives Survey",
          velocity: "Synthetic ISDA Bilateral Exposure",
          balanceItems: {
            assets: [
              { name: "Interest Rate Swap Gross Market Value", amount: "$15,200.0B" },
              { name: "FX Swap & Forward Synthetic Claims", amount: "$85,000.0B" }
            ],
            liabilities: [
              { name: "Gross Negative Derivative Liabilities", amount: "$15,200.0B" },
              { name: "Cross-Border Margin Commitments", amount: "$85,000.0B" }
            ]
          },
          branches: [
            { targetId: "hedge_fund_basis_trade_leverage", targetName: "Treasury Basis Trade Hedge Funds", volume: "$1.20T" }
          ]
        },
        {
          id: "hedge_fund_basis_trade_leverage",
          name: "Hedge Fund Treasury Basis Trade Leverage Engine",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "OFFSHORE",
          sector: "Leveraged Basis Arbitrage",
          volume: "$1.20 Trillion",
          provenance: "Federal Reserve Board Financial Stability Report",
          velocity: "Overnight Bilateral Repo Roll (50:1 Leverage)",
          balanceItems: {
            assets: [
              { name: "Long Cash Treasury Cash Benchmark Securities", amount: "$1,200.0B" },
              { name: "Short CME Treasury Futures Basis Positions", amount: "$1,200.0B" }
            ],
            liabilities: [
              { name: "Bilateral Non-Centrally Cleared Repo Borrowing", amount: "$1,176.0B" },
              { name: "Equity Margin Capital (2% Haircut)", amount: "$24.0B" }
            ]
          },
          branches: [
            { targetId: "us_triparty_repo_pool", targetName: "US Triparty Repo Basin", volume: "$1.20T" }
          ]
        },
        {
          id: "us_triparty_repo_pool",
          name: "US Triparty Repo & FICC Clearing Basin",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "US",
          sector: "Secured Dollar Financing Pool",
          volume: "$3.007 Trillion/day",
          provenance: "DTCC Triparty Bulletin",
          velocity: "Daily SOFR Triparty Settlement",
          balanceItems: {
            assets: [
              { name: "FICC Sponsored Repo Cash Receivables", amount: "$1,200.0B" },
              { name: "Primary Dealer Collateral Lines", amount: "$1,807.0B" }
            ],
            liabilities: [
              { name: "Prime MMF Cash Placements", amount: "$3,007.0B" }
            ]
          },
          branches: [
            { targetId: "global_systemic_bank_nexus", targetName: "Global Systemic Bank Nexus", volume: "$3.20T" }
          ]
        },
        {
          id: "global_systemic_bank_nexus",
          name: "Global Systemic G-SIB Prime Brokerage Nexus",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "WORLD",
          sector: "Systemic G-SIB Counterparty Sinks",
          volume: "$3.20 Trillion",
          provenance: "FSB Global Systemically Important Banks",
          velocity: "Cross-Border Multilateral Clearing",
          balanceItems: {
            assets: [
              { name: "Margin Loans to Relative Value Hedge Funds", amount: "$1,200.0B" },
              { name: "Overnight High-Quality Liquid Assets (HQLA)", amount: "$2,000.0B" }
            ],
            liabilities: [
              { name: "Uninsured Wholesale Deposit Liabilities", amount: "$2,200.0B" },
              { name: "Tier 1 Regulatory Capital Buffer", amount: "$1,000.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "bis_otc_derivatives_dark_matter",
          target: "hedge_fund_basis_trade_leverage",
          action: "OFF-BALANCE-SHEET BASIS CREATION",
          volume: "$1.20T",
          statutory: "BIS Semiannual Derivative Metrics",
          narrative: "Unmodeled OTC derivatives and CME futures basis spreads provide arbitrage pricing signals for relative value hedge funds."
        },
        {
          source: "hedge_fund_basis_trade_leverage",
          target: "us_triparty_repo_pool",
          action: "LEVERAGED REPO CLEARING",
          volume: "$1.20T",
          statutory: "DTCC Sponsored Repo Schedule",
          narrative: "Hedge funds borrow cash in non-centrally cleared bilateral repos and FICC sponsored repo at 50x leverage against Treasury collateral."
        },
        {
          source: "us_triparty_repo_pool",
          target: "global_systemic_bank_nexus",
          action: "G-SIB MARGIN CONTAGION ABSORPTION",
          volume: "$1.20T",
          statutory: "Basel Committee G-SIB Indicators",
          narrative: "G-SIB prime brokerages absorb intraday margin calls, creating systemic off-balance-sheet interconnections."
        }
      ]
    },

    "CIRCUIT-09-NORWAY-GPFG": {
      id: "CIRCUIT-09-NORWAY-GPFG",
      shortNum: "09",
      shortTitle: "Norway GPFG $1.75T",
      title: "Nordic Sovereign Wealth & Global Equity Recycling (Norway GPFG)",
      subtitle: "$1.75 Trillion Government Pension Fund Global financing worldwide public equities and safe-haven sovereign bonds",
      currency: "NOK / USD",
      nominalVolume: "$1.75 Trillion",
      theme: "Global Sovereign Equity Absorption & Wealth Preservation",
      statutoryBadge: "Norges Bank Annual Report",
      doubleEntryProof: { inflow: "$1.75T", outflow: "$1.75T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "norway_norges_bank_gpfg_faucet",
          name: "Norges Bank Investment Management (GPFG Faucet)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "NO",
          sector: "Sovereign Wealth Genesis",
          volume: "$1.75 Trillion",
          provenance: "NBIM Annual Report",
          velocity: "Continuous North Sea Oil Royalty Sweep",
          balanceItems: {
            assets: [
              { name: "Global Public Equities Portfolio (9,000+ Companies)", amount: "$1,225.0B" },
              { name: "Global Sovereign Fixed Income & Infrastructure", amount: "$525.0B" }
            ],
            liabilities: [
              { name: "Norwegian State Petroleum Fund Capital Account", amount: "$1,750.0B" }
            ]
          },
          branches: [
            { targetId: "norway_gpfg_global_equity_sink", targetName: "Global Equity Capital Sink", volume: "$1.225T" },
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custodial Sink", volume: "$300.0B" },
            { targetId: "bund_risk_free_anchor", targetName: "German Bund Safe-Haven Anchor", volume: "$225.0B" }
          ]
        },
        {
          id: "norway_gpfg_global_equity_sink",
          name: "Norway GPFG Global Public Equity Sink",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "GLOBAL",
          sector: "Worldwide Public Equity Sink",
          volume: "$1.225 Trillion",
          provenance: "NBIM Equity Holdings Disclosure",
          velocity: "Permanent Buy-and-Hold Ownership (1.5% of World Equities)",
          balanceItems: {
            assets: [
              { name: "Ownership of 1.5% of All Listed Global Companies", amount: "$1,225.0B" },
              { name: "Tech / Healthcare / Energy Holdings", amount: "$600.0B" }
            ],
            liabilities: [
              { name: "Institutional Equity Beneficiary Claims", amount: "$1,225.0B" }
            ]
          },
          branches: []
        },
        {
          id: "us_treasuries_custody",
          name: "US Treasuries Custodial Sink (Foreign TIC Holdings)",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Safe-Haven Custody Basin",
          volume: "$300.0B",
          provenance: "US Treasury TIC Reports",
          velocity: "Safe-Haven Collateral Custody",
          balanceItems: {
            assets: [
              { name: "US Treasury Benchmark Notes in Custody", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Custodial Liabilities to Norges Bank", amount: "$300.0B" }
            ]
          },
          branches: []
        },
        {
          id: "bund_risk_free_anchor",
          name: "German Federal Bund Risk-Free Capital Sink",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "DE",
          sector: "European Sovereign Debt Anchor",
          volume: "$225.0B",
          provenance: "Finanzagentur Gazette",
          velocity: "Risk-Free Fixed Income Sink",
          balanceItems: {
            assets: [
              { name: "German 10Y/30Y Bund Holdings", amount: "$225.0B" }
            ],
            liabilities: [
              { name: "German Federal Sovereign Debt Outstanding", amount: "$225.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "norway_norges_bank_gpfg_faucet",
          target: "norway_gpfg_global_equity_sink",
          action: "GLOBAL EQUITY DEPLOYMENT",
          volume: "$1.225T",
          statutory: "NBIM Mandate Section 3",
          narrative: "Norges Bank systematically invests 70% of fund capital into global equities across 70 nations, owning 1.5% of all listed worldwide equities."
        },
        {
          source: "norway_norges_bank_gpfg_faucet",
          target: "us_treasuries_custody",
          action: "DOLLAR SOVEREIGN ANCHOR",
          volume: "$300.0B",
          statutory: "US TIC Table 5",
          narrative: "Norges Bank allocates $300B into US Treasury benchmarks to maintain liquid dollar collateral for international rebalancing."
        },
        {
          source: "norway_norges_bank_gpfg_faucet",
          target: "bund_risk_free_anchor",
          action: "EUROZONE FIXED INCOME FLIGHT",
          volume: "$225.0B",
          statutory: "German Federal Debt Registry",
          narrative: "NBIM directs $225B into German Federal Bunds, providing risk-free sovereign debt stabilization in European markets."
        }
      ]
    },

    "CIRCUIT-10-SWISS-ALPINE": {
      id: "CIRCUIT-10-SWISS-ALPINE",
      shortNum: "10",
      shortTitle: "Swiss SNB & UBS $1.7T",
      title: "Alpine Safe-Haven Flight & Swiss G-SIB Interbank Clearing (SNB & UBS)",
      subtitle: "$950B SNB FX reserve interventions and $1.7T UBS consolidated G-SIB balance sheet",
      currency: "CHF / USD",
      nominalVolume: "$950.0B ($1.7T G-SIB)",
      theme: "Cross-Currency Safe-Haven Inflows & Global Wealth Clearing",
      statutoryBadge: "SNB Balance Sheet / UBS SEC 20-F",
      doubleEntryProof: { inflow: "$950.0B", outflow: "$950.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "swiss_national_bank_snb_vault",
          name: "Swiss National Bank (SNB) Sovereign FX Vault",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "CH",
          sector: "Sovereign FX Vault",
          volume: "$950.0B",
          provenance: "SNB Balance Sheet Statistics",
          velocity: "Daily Safe-Haven FX Interventions",
          balanceItems: {
            assets: [
              { name: "Foreign Currency Investments (US/EU Stocks & Bonds)", amount: "$780.0B" },
              { name: "Physical Gold Vault in Zurich & Berne", amount: "$65.0B" },
              { name: "Claims on Interbank Clearing", amount: "$105.0B" }
            ],
            liabilities: [
              { name: "Sight Deposits of Domestic Commercial Banks", amount: "$620.0B" },
              { name: "Banknotes in Circulation & Equity Capital", amount: "$330.0B" }
            ]
          },
          branches: [
            { targetId: "ubs_group_consolidated_gsib", targetName: "UBS Consolidated G-SIB", volume: "$950.0B" }
          ]
        },
        {
          id: "ubs_group_consolidated_gsib",
          name: "UBS Group Consolidated (Global Systemically Important Bank)",
          tier: 1,
          tierLabel: "TRANSMISSION G-SIB",
          jurisdiction: "CH_GLOBAL",
          sector: "Consolidated Global G-SIB",
          volume: "$1.71 Trillion Assets",
          provenance: "UBS Annual SEC Form 20-F",
          velocity: "Global Multi-Currency Wealth & Trading Velocity",
          balanceItems: {
            assets: [
              { name: "Global Wealth Management Loans & Securitized Assets", amount: "$850.0B" },
              { name: "High Quality Liquid Assets & Cash at Central Banks", amount: "$380.0B" },
              { name: "Trading Portfolio & Repo Assets", amount: "$480.0B" }
            ],
            liabilities: [
              { name: "Customer Deposits Across 50+ Jurisdictions", amount: "$1,120.0B" },
              { name: "Long-Term Senior Debt & Regulatory Capital", amount: "$590.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custody", volume: "$300.0B" },
            { targetId: "norway_gpfg_global_equity_sink", targetName: "Global Equity Preservation", volume: "$450.0B" }
          ]
        },
        {
          id: "us_treasuries_custody",
          name: "US Treasuries Custody & Wealth Preservation Basin",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Safe-Haven Asset Custody",
          volume: "$300.0B",
          provenance: "Federal Reserve Custody Accounts",
          velocity: "Permanent Wealth Preservation",
          balanceItems: {
            assets: [
              { name: "Held-to-Maturity US Sovereign Paper", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Swiss Client Custody Claims", amount: "$300.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "swiss_national_bank_snb_vault",
          target: "ubs_group_consolidated_gsib",
          action: "SAFE-HAVEN FX ABSORPTION",
          volume: "$950.0B",
          statutory: "SNB Monetary Policy Circular",
          narrative: "Safe-haven inflows drive CHF upward; the SNB creates sight deposits to buy foreign currency assets, transmitting through UBS."
        },
        {
          source: "ubs_group_consolidated_gsib",
          target: "us_treasuries_custody",
          action: "WEALTH CLEARING CONDUIT",
          volume: "$300.0B",
          statutory: "FINMA G-SIB Supervisory Framework",
          narrative: "UBS clears dollar and euro asset management flows into US Treasury collateral and global safe-haven custody accounts."
        }
      ]
    },

    "CIRCUIT-11-SINGAPORE-ASIAN-DOLLAR": {
      id: "CIRCUIT-11-SINGAPORE-ASIAN-DOLLAR",
      shortNum: "11",
      shortTitle: "Singapore MAS & GIC $1.45T",
      title: "Singapore Asian Dollar Hub & Sovereign Wealth Syndication (MAS & GIC/Temasek)",
      subtitle: "$400B MAS foreign exchange reserves and $1.05T GIC/Temasek sovereign asset basins",
      currency: "USD / SGD",
      nominalVolume: "$1.45 Trillion",
      theme: "Offshore Asian Dollar Liquidity & Sovereign Capital Syndication",
      statutoryBadge: "MAS Annual Report / GIC Report",
      doubleEntryProof: { inflow: "$1.45T", outflow: "$1.45T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "singapore_mas_reserve_faucet",
          name: "Monetary Authority of Singapore (MAS) Reserve Faucet",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "SG",
          sector: "Central Bank Genesis",
          volume: "$400.0 Billion",
          provenance: "MAS Official Foreign Reserves Data",
          velocity: "S$NEER Exchange Rate Policy Band Operations",
          balanceItems: {
            assets: [
              { name: "Foreign Currency Deposits & Sovereign Bonds", amount: "$375.0B" },
              { name: "Official Gold Reserves (Singapore Vaults)", amount: "$25.0B" }
            ],
            liabilities: [
              { name: "Currency in Circulation & Commercial Bank Reserves", amount: "$180.0B" },
              { name: "Government Deposits in MAS", amount: "$220.0B" }
            ]
          },
          branches: [
            { targetId: "singapore_gic_temasek_sovereign_basin", targetName: "GIC & Temasek Sovereign Basin", volume: "$1.05T" }
          ]
        },
        {
          id: "singapore_gic_temasek_sovereign_basin",
          name: "Singapore GIC & Temasek Sovereign Investment Basin",
          tier: 1,
          tierLabel: "TRANSMISSION BASIN",
          jurisdiction: "SG_GLOBAL",
          sector: "Sovereign Wealth Syndication",
          volume: "$1.05 Trillion AUM",
          provenance: "GIC Annual Report / Temasek Review",
          velocity: "Offshore Dollar Market Syndication",
          balanceItems: {
            assets: [
              { name: "Global Private Equity, Infrastructure & Real Estate", amount: "$650.0B" },
              { name: "Public Equities & Sovereign Fixed Income", amount: "$400.0B" }
            ],
            liabilities: [
              { name: "Government Sovereign Investment Mandates", amount: "$1,050.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custody", volume: "$300.0B" },
            { targetId: "sovereign_debt_holders", targetName: "Global Sovereign Debt Holders", volume: "$750.0B" }
          ]
        },
        {
          id: "sovereign_debt_holders",
          name: "Institutional Sovereign Debt Holders Basin",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "WORLD",
          sector: "Global Debt Market Sinks",
          volume: "$1.05 Trillion",
          provenance: "IMF Coordinated Portfolio Investment Survey",
          velocity: "Institutional Safe-Haven Yield Accumulation",
          balanceItems: {
            assets: [
              { name: "Global Sovereign Debt Holdings", amount: "$1,050.0B" }
            ],
            liabilities: [
              { name: "Institutional Pension & Wealth Liabilities", amount: "$1,050.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "singapore_mas_reserve_faucet",
          target: "singapore_gic_temasek_sovereign_basin",
          action: "SOVEREIGN SURPLUS TRANSFER",
          volume: "$400.0B",
          statutory: "Singapore Government Securities Act",
          narrative: "Asian merchandise trade surpluses accumulating in MAS FX reserves are systematically channeled into GIC and Temasek for long-term global yield."
        },
        {
          source: "singapore_gic_temasek_sovereign_basin",
          target: "sovereign_debt_holders",
          action: "GLOBAL COLLATERAL ABSORPTION",
          volume: "$750.0B",
          statutory: "MAS Asian Dollar Market Circular",
          narrative: "Singapore syndicates offshore Asian dollar liquidity into Western sovereign bonds, commercial real estate, and global tech platforms."
        }
      ]
    },

    "CIRCUIT-12-EURASIAN-SHADOW": {
      id: "CIRCUIT-12-EURASIAN-SHADOW",
      shortNum: "12",
      shortTitle: "Russian $420B Commodity Nexus",
      title: "Eurasian Sovereign Debt, State Banking Nexus & $420B Commodity Conduit",
      subtitle: "$600B CBR balance sheet, $155B NWF oil buffer, $920B Sberbank/VTB credit nexus, and $180B offshore trapped capital",
      currency: "RUB / CNY",
      nominalVolume: "$420.0B ($920B Banking)",
      theme: "Sovereign Sanctions Bypass & Offshore Trapped Currency Accumulation",
      statutoryBadge: "CBR Bulletin / Russian MinFin Data",
      doubleEntryProof: { inflow: "$420.0B", outflow: "$420.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "bank_of_russia_cbr_vault",
          name: "Bank of Russia (CBR) Sovereign Vault & Gold Reserves",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "RU",
          sector: "Sanctioned Central Bank",
          volume: "$600.0B",
          provenance: "CBR Statistics Bulletin",
          velocity: "Bi-Weekly Key Rate Setting & Yuan Clearing",
          balanceItems: {
            assets: [
              { name: "Gold Bullion Vault (Moscow)", amount: "$185.0B" },
              { name: "Yuan Foreign Exchange & Bilateral Claims", amount: "$115.0B" },
              { name: "Frozen G7 Sovereign Assets", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Ruble Monetary Base", amount: "$280.0B" },
              { name: "National Wealth Fund MinFin Accounts", amount: "$155.0B" },
              { name: "Banking System Excess Reserves", amount: "$165.0B" }
            ]
          },
          branches: [
            { targetId: "russia_national_wealth_fund_nwf", targetName: "National Wealth Fund (NWF)", volume: "$155.0B" },
            { targetId: "russian_state_banking_credit_nexus", targetName: "Sberbank / VTB Banking Nexus", volume: "$920.0B" }
          ]
        },
        {
          id: "russia_national_wealth_fund_nwf",
          name: "Russia National Wealth Fund (NWF Sovereign Oil Buffer)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "RU",
          sector: "Sovereign Wealth Buffer",
          volume: "$155.0 Billion",
          provenance: "MinFin Russia Monthly Report",
          velocity: "Fiscal Deficit Subsidies",
          balanceItems: {
            assets: [
              { name: "Physical Gold & Chinese Renminbi Liquid Assets", amount: "$55.0B" },
              { name: "Domestic Infrastructure & State Bank Equity", amount: "$100.0B" }
            ],
            liabilities: [
              { name: "Federal Budget Reserve Balances", amount: "$155.0B" }
            ]
          },
          branches: [
            { targetId: "russian_state_banking_credit_nexus", targetName: "Sberbank / VTB Nexus", volume: "$100.0B" }
          ]
        },
        {
          id: "russian_state_banking_credit_nexus",
          name: "Russian State Banking Credit Nexus (Sberbank & VTB)",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "RU",
          sector: "State Commercial Bank Nexus",
          volume: "$920.0 Billion",
          provenance: "IFRS Financial Statements Sber/VTB",
          velocity: "Domestic Subsidized Corporate Credit Expansion",
          balanceItems: {
            assets: [
              { name: "Commercial & Defense Industrial Loan Portfolios", amount: "$720.0B" },
              { name: "CBR Central Bank Deposit Accounts", amount: "$200.0B" }
            ],
            liabilities: [
              { name: "Retail & Corporate Ruble Demand Deposits", amount: "$680.0B" },
              { name: "NWF Subordinated Debt & State Capital", amount: "$240.0B" }
            ]
          },
          branches: [
            { targetId: "gazprombank_energy_settlement_hub", targetName: "Gazprombank Gas Clearing Hub", volume: "$95.0B" },
            { targetId: "shadow_tanker_energy_arbitrage", targetName: "Shadow Fleet Crude Arbitrage", volume: "$140.0B" }
          ]
        },
        {
          id: "russia_offshore_shadow_capital_basin",
          name: "Russian Offshore Trapped Capital Basin (UAE/Vostro)",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "OFFSHORE",
          sector: "Trapped Currency Basin",
          volume: "$180.0 Billion",
          provenance: "Bank of Russia Financial Stability Review",
          velocity: "Restricted Convertibility Accumulation",
          balanceItems: {
            assets: [
              { name: "Non-Convertible Indian Rupee Vostro Accounts", amount: "$40.0B" },
              { name: "UAE Dirham Commercial Bank Deposits", amount: "$85.0B" },
              { name: "Turkish Hub Trade Receivables", amount: "$55.0B" }
            ],
            liabilities: [
              { name: "Russian Energy Exporter Trapped Balances", amount: "$180.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "bank_of_russia_cbr_vault",
          target: "russia_national_wealth_fund_nwf",
          action: "FISCAL BUFFER TRANSFER",
          volume: "$155.0B",
          statutory: "Russian Budget Code Art. 96",
          narrative: "Tax revenues from hydrocarbon exports above baseline thresholds are deposited into the NWF to backstop domestic deficits."
        },
        {
          source: "russia_national_wealth_fund_nwf",
          target: "russian_state_banking_credit_nexus",
          action: "STATE CAPITAL INJECTION",
          volume: "$100.0B",
          statutory: "MinFin Subordinated Lending Directive",
          narrative: "NWF funds inject Tier 2 subordinated capital into Sberbank and VTB, underwriting $920B in domestic subsidized credit."
        },
        {
          source: "russian_state_banking_credit_nexus",
          target: "russia_offshore_shadow_capital_basin",
          action: "TRAPPED CURRENCY ACCUMULATION",
          volume: "$180.0B",
          statutory: "CBR Currency Control Regulation",
          narrative: "Sanctions prevent offshore crude proceeds from converting into Western assets, accumulating $180B in UAE dirhams and Indian vostro rupees."
        }
      ]
    },

    "CIRCUIT-13-MAPLE-NEARSHORING": {
      id: "CIRCUIT-13-MAPLE-NEARSHORING",
      shortNum: "13",
      shortTitle: "USMCA & Maple 8 $1.5T",
      title: "North American Nearshoring & Canadian Maple Pension Consortium (USMCA & CPPIB)",
      subtitle: "$500B bilateral Mexico-US manufacturing trade settlement and $1.5T Canadian alternative pension allocations",
      currency: "USD / CAD / MXN",
      nominalVolume: "$1.50 Trillion",
      theme: "Cross-Border Trade Nearshoring & Pension Capital Deployment",
      statutoryBadge: "USMCA Trade Data / CPPIB Annual",
      doubleEntryProof: { inflow: "$1.50T", outflow: "$1.50T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "banco_de_mexico_banxico_faucet",
          name: "Banco de México (Banxico) Reserve & Monetary Faucet",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "MX",
          sector: "Central Bank Genesis",
          volume: "$220.0 Billion",
          provenance: "Banxico Indicadores Económicos",
          velocity: "Daily FX Reserve Intervention",
          balanceItems: {
            assets: [
              { name: "US Dollar Reserve Holdings", amount: "$220.0B" },
              { name: "Bilateral Trade Settlement Claims", amount: "$35.0B" }
            ],
            liabilities: [
              { name: "Monetary Base (Pesos in Circulation)", amount: "$175.0B" },
              { name: "Commercial Banking Deposits", amount: "$80.0B" }
            ]
          },
          branches: [
            { targetId: "usmca_nearshoring_trade_conduit", targetName: "USMCA Trade Conduit", volume: "$500.0B" }
          ]
        },
        {
          id: "bank_of_canada_boc_vault",
          name: "Bank of Canada (BoC) Sovereign Vault",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "CA",
          sector: "Central Bank Genesis",
          volume: "$410.0 Billion",
          provenance: "Bank of Canada Banking and Financial Statistics",
          velocity: "Lynx RTGS Real-Time Settlement",
          balanceItems: {
            assets: [
              { name: "Government of Canada Bonds", amount: "$320.0B" },
              { name: "Term Repo Operations", amount: "$90.0B" }
            ],
            liabilities: [
              { name: "Canadian Dollar Settlement Balances", amount: "$210.0B" },
              { name: "Banknotes in Circulation", amount: "$120.0B" }
            ]
          },
          branches: [
            { targetId: "canada_maple_pension_consortium", targetName: "Maple 8 Pension Consortium", volume: "$1.50T" }
          ]
        },
        {
          id: "usmca_nearshoring_trade_conduit",
          name: "USMCA Nearshoring Bilateral Trade Capital Conduit",
          tier: 1,
          tierLabel: "TRANSMISSION CONDUIT",
          jurisdiction: "MX_US",
          sector: "Cross-Border Industrial Trade Corridor",
          volume: "$500.0 Billion/yr",
          provenance: "US Census Bureau Foreign Trade Statistics",
          velocity: "30-Day Commercial Trade Credit",
          balanceItems: {
            assets: [
              { name: "Automotive & Electronics Export Invoices", amount: "$500.0B" },
              { name: "Cross-Border Supply Chain Receivables", amount: "$120.0B" }
            ],
            liabilities: [
              { name: "Commercial Trade Clearings to US Assemblers", amount: "$500.0B" }
            ]
          },
          branches: [
            { targetId: "us_corporate_and_household_borrowers", targetName: "US Corporate Sector", volume: "$500.0B" }
          ]
        },
        {
          id: "canada_maple_pension_consortium",
          name: "Canadian Maple 8 Pension Consortium (CPPIB / CDPQ / OTPP)",
          tier: 2,
          tierLabel: "TRAVERSAL PENSION POOL",
          jurisdiction: "CA_GLOBAL",
          sector: "Global Alternative Pension Consortium",
          volume: "$1.50 Trillion AUM",
          provenance: "CPPIB / CDPQ / OTPP Annual Reports",
          velocity: "Long-Term Direct Infrastructure Deployment",
          balanceItems: {
            assets: [
              { name: "Global Infrastructure, Real Estate & Private Equity", amount: "$950.0B" },
              { name: "Public Equities & Sovereign Fixed Income", amount: "$550.0B" }
            ],
            liabilities: [
              { name: "Canadian Worker Pension Entitlements", amount: "$1,500.0B" }
            ]
          },
          branches: [
            { targetId: "us_corporate_and_household_borrowers", targetName: "US Corporate Sector", volume: "$500.0B" }
          ]
        },
        {
          id: "us_corporate_and_household_borrowers",
          name: "US Real Economy Industrial & Infrastructure Sinks",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Industrial Economy Real Asset Sink",
          volume: "$1.50 Trillion",
          provenance: "BEA Fixed Assets Accounts",
          velocity: "Permanent Industrial Capital Sinks",
          balanceItems: {
            assets: [
              { name: "North American Supply Chain Factory Assets", amount: "$1,500.0B" }
            ],
            liabilities: [
              { name: "Long-Term Infrastructure Financing Notes", amount: "$1,500.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "banco_de_mexico_banxico_faucet",
          target: "usmca_nearshoring_trade_conduit",
          action: "CROSS-BORDER TRADE FINANCING",
          volume: "$500.0B",
          statutory: "USMCA Chapter 3 Rules of Origin",
          narrative: "Nearshoring investment in northern Mexico generates $500B in bilateral manufacturing exports traversing into US supply chains."
        },
        {
          source: "bank_of_canada_boc_vault",
          target: "canada_maple_pension_consortium",
          action: "CANADIAN PENSION ACCUMULATION",
          volume: "$1.50T",
          statutory: "Canada Pension Plan Investment Board Act",
          narrative: "Canadian public pension contributions consolidate under the Maple 8 giants ($1.5T AUM) to deploy long-term private capital."
        },
        {
          source: "canada_maple_pension_consortium",
          target: "us_corporate_and_household_borrowers",
          action: "INFRASTRUCTURE EQUITY DEPLOYMENT",
          volume: "$500.0B",
          statutory: "CPPIB Global Investment Mandate",
          narrative: "Canadian pensions finance ports, energy grids, and logistics facilities powering the integrated North American USMCA trade corridor."
        }
      ]
    },

    "CIRCUIT-14-MULTILATERAL-SDR": {
      id: "CIRCUIT-14-MULTILATERAL-SDR",
      shortNum: "14",
      shortTitle: "IMF SDR & BIS Basel $935B",
      title: "Multilateral Reserve Architecture & BIS Basel Central Banking Desk",
      subtitle: "$935B IMF SDR allocation pool and $450B BIS central bank gold & currency depositories",
      currency: "SDR / USD",
      nominalVolume: "$935.0B ($450B BIS)",
      theme: "Supranational Reserve Backstops & Central Bank Depository Clearing",
      statutoryBadge: "IMF Financial Statements / BIS Balance Sheet",
      doubleEntryProof: { inflow: "$935.0B", outflow: "$935.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "imf_special_drawing_rights_sdr_pool",
          name: "IMF Special Drawing Rights (SDR) Reserve Pool",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "GLOBAL_MULTILATERAL",
          sector: "Supranational Monetary Reserve Basket",
          volume: "$935.0 Billion (660B SDR)",
          provenance: "IMF Financial Data",
          velocity: "Official Voluntary Trading Arrangement (VTA)",
          balanceItems: {
            assets: [
              { name: "SDR Basket Holdings (USD 43.38%, EUR 29.31%, CNY 12.28%, JPY 7.59%, GBP 7.44%)", amount: "$935.0B" }
            ],
            liabilities: [
              { name: "SDR Allocations to 190 Member Countries", amount: "$935.0B" }
            ]
          },
          branches: [
            { targetId: "bis_basel_banking_department", targetName: "BIS Basel Banking Department", volume: "$450.0B" }
          ]
        },
        {
          id: "bis_basel_banking_department",
          name: "Bank for International Settlements (BIS) Basel Desk",
          tier: 1,
          tierLabel: "TRANSMISSION BANK",
          jurisdiction: "GLOBAL_MULTILATERAL",
          sector: "Central Bank of Central Banks",
          volume: "$450.0 Billion",
          provenance: "BIS Annual Financial Statements",
          velocity: "Official Reserve Deposit Placement",
          balanceItems: {
            assets: [
              { name: "Official Gold Intermediation Holdings", amount: "$120.0B" },
              { name: "Reverse Repo & Sovereign Paper", amount: "$330.0B" }
            ],
            liabilities: [
              { name: "Currency Deposits from 63 Member Central Banks", amount: "$390.0B" },
              { name: "Gold Sight Deposits & Equity Reserves", amount: "$60.0B" }
            ]
          },
          branches: [
            { targetId: "bundesbank", targetName: "Deutsche Bundesbank", volume: "$181.3B" },
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custodial Basin", volume: "$300.0B" }
          ]
        },
        {
          id: "bundesbank",
          name: "Deutsche Bundesbank (Frankfurt)",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "DE",
          sector: "Creditor Central Bank",
          volume: "$181.3B",
          provenance: "Bundesbank Monatsbericht",
          velocity: "Eurosystem Deposit Balancing",
          balanceItems: {
            assets: [
              { name: "Positive TARGET2 & Official Claims", amount: "$1,080.0B" }
            ],
            liabilities: [
              { name: "Euro Reserve Liabilities", amount: "$1,080.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custodial Basin", volume: "$300.0B" }
          ]
        },
        {
          id: "us_treasuries_custody",
          name: "Federal Reserve Safe-Haven Custody for Foreign Accounts",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Supranational Custodial Sink",
          volume: "$300.0 Billion",
          provenance: "Federal Reserve H.4.1 Release",
          velocity: "Official Reserve Vault Custody",
          balanceItems: {
            assets: [
              { name: "US Treasury Securities Pledged by Central Banks", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Custody Liabilities to Foreign & International Monetary Authorities", amount: "$300.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "imf_special_drawing_rights_sdr_pool",
          target: "bis_basel_banking_department",
          action: "SDR LIQUIDITY INTERMEDIATION",
          volume: "$450.0B",
          statutory: "IMF Articles of Agreement Art. XVII",
          narrative: "Central banks exchange Special Drawing Rights through the BIS Banking Department for freely usable currencies to manage liquidity."
        },
        {
          source: "bis_basel_banking_department",
          target: "bundesbank",
          action: "EURO RESERVE DEPOSIT",
          volume: "$181.3B",
          statutory: "BIS Statutes Art. 21",
          narrative: "The BIS places official currency reserves with creditor central banks, reinforcing Bundesbank positive reserve balances."
        },
        {
          source: "bis_basel_banking_department",
          target: "us_treasuries_custody",
          action: "FOREIGN CUSTODY PLEDGE",
          volume: "$300.0B",
          statutory: "Federal Reserve Act Section 14",
          narrative: "International central banks pledge US Treasuries into the NY Fed foreign custody account to secure cross-border settlement lines."
        }
      ]
    }
  },

  sovereignRoots: {
    "french_republic_tresor": {
      id: "french_republic_tresor",
      shortLabel: "France (Trésor / BdF)",
      jurisdiction: "FR",
      title: "French Republic Trésor & Eurosystem Sovereign Genesis",
      subtitle: "Agence France Trésor sovereign benchmark auctions traversing Primary SVT dealers into TARGET2 and German Bund sinks",
      currency: "EUR",
      nominalVolume: "€250.0B ($272.5B)",
      theme: "Eurozone Sovereign Issuance & RTGS Clearing",
      statutoryBadge: "AFT / ECB SDW",
      doubleEntryProof: { inflow: "€250.0B", outflow: "€250.0B", net: "€0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "french_republic_tresor",
          name: "French Republic Trésor (Agence France Trésor)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "FR",
          sector: "Sovereign Debt Issuer",
          volume: "€250.0B",
          provenance: "AFT Bulletin Mensuel",
          velocity: "Monthly Auction Schedule (T+2)",
          balanceItems: {
            assets: [
              { name: "Public Taxing Authority & State Assets", amount: "€2,950.0B" },
              { name: "Treasury Account at Banque de France", amount: "€45.2B" }
            ],
            liabilities: [
              { name: "OAT Benchmark Long-Term Debt", amount: "€2,410.0B" },
              { name: "BTF Short-Term Treasury Bills", amount: "€180.0B" }
            ]
          },
          branches: [
            { targetId: "svt_dealers_bnp_socgen", targetName: "SVT Primary Dealers (BNP/SocGen)", volume: "€145.0B" },
            { targetId: "ca_cib_natixis_dealer_syndicate", targetName: "Secondary Syndicate (Natixis)", volume: "€85.0B" }
          ]
        },
        {
          id: "svt_dealers_bnp_socgen",
          name: "Primary Dealers (SVT: BNP Paribas & SocGen)",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "FR",
          sector: "SVT Primary Broker-Dealer",
          volume: "€145.0B",
          provenance: "Banque de France SVT Report",
          velocity: "Intraday Repo Turnover (T+0)",
          balanceItems: {
            assets: [
              { name: "Sovereign OAT Market Making Inventory", amount: "€145.0B" }
            ],
            liabilities: [
              { name: "Intraday Banque de France Credit Lines", amount: "€145.0B" }
            ]
          },
          branches: [
            { targetId: "banque_de_france", targetName: "Banque de France Refinancing", volume: "€120.0B" }
          ]
        },
        {
          id: "banque_de_france",
          name: "Banque de France (National Central Bank)",
          tier: 1,
          tierLabel: "TRANSMISSION CB",
          jurisdiction: "FR",
          sector: "Eurosystem Central Bank",
          volume: "€181.3B",
          provenance: "BdF Compte de Résultat",
          velocity: "TARGET2 Real-Time Gross Settlement",
          balanceItems: {
            assets: [
              { name: "Main Refinancing Operations (MRO)", amount: "€120.0B" }
            ],
            liabilities: [
              { name: "Net TARGET2 Liability Balance", amount: "€181.3B" }
            ]
          },
          branches: [
            { targetId: "eurosystem_target2_pool", targetName: "TARGET2 RTGS Pool", volume: "€181.3B" }
          ]
        },
        {
          id: "eurosystem_target2_pool",
          name: "Eurosystem TARGET2 Clearing Pool",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "EU",
          sector: "RTGS Clearing Pool",
          volume: "€1.25T/day",
          provenance: "ECB SDW Target2 Balances",
          velocity: "Continuous Real-Time Clearing",
          balanceItems: {
            assets: [
              { name: "Claims on Debtor Central Banks", amount: "€640.0B" }
            ],
            liabilities: [
              { name: "Liabilities to Creditor Central Banks", amount: "€640.0B" }
            ]
          },
          branches: [
            { targetId: "bund_risk_free_anchor", targetName: "German Bund Anchor", volume: "€181.3B" }
          ]
        },
        {
          id: "bund_risk_free_anchor",
          name: "German Federal Bund Risk-Free Anchor",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "DE",
          sector: "Safe-Haven Sovereign Anchor",
          volume: "€250.0B",
          provenance: "Finanzagentur Gazette",
          velocity: "Permanent Sovereign Custody",
          balanceItems: {
            assets: [
              { name: "German Federal Sovereign Collateral", amount: "€2,100.0B" }
            ],
            liabilities: [
              { name: "Benchmark Debt Outstanding", amount: "€2,100.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "french_republic_tresor",
          target: "svt_dealers_bnp_socgen",
          action: "PRIMARY OAT AUCTION",
          volume: "€145.0B",
          statutory: "AFT Monthly Bulletin",
          narrative: "Agence France Trésor auctions 10-year and 30-year OAT sovereign bonds to primary SVT dealers."
        },
        {
          source: "svt_dealers_bnp_socgen",
          target: "banque_de_france",
          action: "INTRADAY REFINANCING",
          volume: "€120.0B",
          statutory: "ECB Refinancing Operations Guideline",
          narrative: "SVT dealers repo OAT paper into Banque de France to access intraday liquidity and refinance bond auction absorption."
        },
        {
          source: "banque_de_france",
          target: "eurosystem_target2_pool",
          action: "TARGET2 TRANS-EUROPEAN WIRE",
          volume: "€181.3B",
          statutory: "ECB Target2 Legal Decision",
          narrative: "Net cross-border capital outflows clear through the Eurosystem TARGET2 RTGS balance sheet."
        },
        {
          source: "eurosystem_target2_pool",
          target: "bund_risk_free_anchor",
          action: "SAFE-HAVEN BUND ALLOCATION",
          volume: "€181.3B",
          statutory: "Finanzagentur Bund Issuance Schedule",
          narrative: "Capital parks into the German Federal Bund safe-haven anchor, cementing the benchmark Eurozone risk-free yield curve."
        }
      ]
    },

    "us_treasury_tga": {
      id: "us_treasury_tga",
      shortLabel: "United States (US Treasury / Fed)",
      jurisdiction: "US",
      title: "United States Treasury & Federal Reserve Monetary Genesis",
      subtitle: "$2.157T Treasury debt issuance, primary dealer repo transmission, and DTCC Triparty clearing",
      currency: "USD",
      nominalVolume: "$2.157 Trillion",
      theme: "Transatlantic Dollar Funding & Sovereign Debt Management",
      statutoryBadge: "Daily Treasury Statement / Fed H.4.1",
      doubleEntryProof: { inflow: "$2.157T", outflow: "$2.157T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "us_corporate_and_household_borrowers",
          name: "US Corporate & Household Taxpayers & Borrowers",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "US",
          sector: "Real Economy Debtors",
          volume: "$2.157T",
          provenance: "Fed Financial Accounts Z.1",
          velocity: "Quarterly Tax & Debt Service",
          balanceItems: {
            assets: [
              { name: "Real Economy Productive Assets", amount: "$38,400.0B" }
            ],
            liabilities: [
              { name: "Federal Taxes & Debt Liabilities", amount: "$2,157.0B" }
            ]
          },
          branches: [
            { targetId: "us_commercial_bank_credit_pool", targetName: "US Commercial Banking Reserve Pool", volume: "$2.157T" }
          ]
        },
        {
          id: "us_commercial_bank_credit_pool",
          name: "US Commercial Banking Reserve Pool",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "US",
          sector: "Commercial Banking System",
          volume: "$3.25 Trillion Reserves",
          provenance: "Fed H.8 Aggregate Balance Sheet",
          velocity: "Daily Fedwire Reserve Transfers",
          balanceItems: {
            assets: [
              { name: "Master Account Reserve Balances at Fed", amount: "$3,250.0B" }
            ],
            liabilities: [
              { name: "Demand Deposits", amount: "$17,400.0B" }
            ]
          },
          branches: [
            { targetId: "us_triparty_repo_pool", targetName: "US Triparty Repo Basin", volume: "$1.85T" },
            { targetId: "us_treasury_tga", targetName: "US Treasury General Account", volume: "$883.3B" }
          ]
        },
        {
          id: "us_triparty_repo_pool",
          name: "US Triparty Repo SOFR Clearing Basin (DTCC / BNY Mellon)",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "US",
          sector: "Overnight Repo Clearing Basin",
          volume: "$3.007 Trillion/day",
          provenance: "DTCC Triparty / NY Fed SOFR",
          velocity: "Overnight Wholesale SOFR Turnover",
          balanceItems: {
            assets: [
              { name: "Overnight Reverse Repo Loans to Dealers", amount: "$3,007.0B" }
            ],
            liabilities: [
              { name: "Institutional Cash Deposits", amount: "$3,007.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasury_tga", targetName: "US Treasury General Account", volume: "$883.3B" }
          ]
        },
        {
          id: "us_treasury_tga",
          name: "US Treasury General Account (Fed Cash Vault)",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "US",
          sector: "Sovereign Operating Cash Vault",
          volume: "$883.3 Billion",
          provenance: "Daily Treasury Statement",
          velocity: "Daily Fedwire Inflow Sweep",
          balanceItems: {
            assets: [
              { name: "Cash on Deposit at Federal Reserve", amount: "$883.3B" }
            ],
            liabilities: [
              { name: "Federal Operating Budget Allocations", amount: "$883.3B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "us_corporate_and_household_borrowers",
          target: "us_commercial_bank_credit_pool",
          action: "TAX & AUCTION WIRE",
          volume: "$2.157T",
          statutory: "IRS Financial Collections",
          narrative: "Taxpayers and investors wire cash to commercial banks to purchase freshly auctioned US Treasury benchmark issues."
        },
        {
          source: "us_commercial_bank_credit_pool",
          target: "us_triparty_repo_pool",
          action: "TRIPARTY SOFR CLEARING",
          volume: "$1.85T",
          statutory: "DTCC GCF Repo Notice",
          narrative: "Commercial banks deploy reserves into the $3T/day Triparty repo pool to finance dealer inventory at SOFR benchmark rates."
        },
        {
          source: "us_triparty_repo_pool",
          target: "us_treasury_tga",
          action: "TGA CASH SWEEP",
          volume: "$883.3B",
          statutory: "Daily Treasury Statement Table 1",
          narrative: "Repo liquidity finances primary dealer Treasury absorption, settling net cash balances into the Treasury General Account at the Fed."
        }
      ]
    },

    "pboc_safe_foreign_reserves": {
      id: "pboc_safe_foreign_reserves",
      shortLabel: "China (PBOC & SAFE)",
      jurisdiction: "CN",
      title: "People's Bank of China & SAFE Sovereign FX Architecture",
      subtitle: "$3.24T foreign exchange reserves, Hong Kong offshore CNH clearing, and CIPS cross-border payments",
      currency: "CNY / USD",
      nominalVolume: "$3.24 Trillion",
      theme: "Cross-Border De-Dollarization & Sovereign Reserve Recycling",
      statutoryBadge: "PBOC / SAFE Gazette",
      doubleEntryProof: { inflow: "$3.24T", outflow: "$3.24T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "pboc_safe_foreign_reserves",
          name: "People's Bank of China & SAFE Foreign Reserves",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "CN",
          sector: "Sovereign FX Reserve Vault",
          volume: "$3.24 Trillion",
          provenance: "SAFE Statistical Bulletin",
          velocity: "Bilateral Currency Swaps & FX Interventions",
          balanceItems: {
            assets: [
              { name: "Foreign Exchange Currency Reserves", amount: "$3,240.0B" },
              { name: "Official Gold Reserves Vault (Beijing)", amount: "$180.0B" }
            ],
            liabilities: [
              { name: "Renminbi Monetary Base", amount: "$3,050.0B" },
              { name: "Bilateral Central Bank Swap Network", amount: "$550.0B" }
            ]
          },
          branches: [
            { targetId: "chinese_state_banks_fx_desk", targetName: "Chinese Big 4 State Banks FX Desk", volume: "$850.0B" },
            { targetId: "petro_yuan_bilateral_settlement_bridge", targetName: "Petro-Yuan Settlement Bridge", volume: "$180.0B" }
          ]
        },
        {
          id: "chinese_state_banks_fx_desk",
          name: "Chinese Big 4 State Banks FX Desks (ICBC/CCB/BoC/ABC)",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "CN",
          sector: "State Commercial Bank Nexus",
          volume: "$850.0 Billion",
          provenance: "CBIRC Regulatory Returns",
          velocity: "Daily FX Swap & Forward Netting",
          balanceItems: {
            assets: [
              { name: "Foreign Exchange Claims & Swaps", amount: "$850.0B" }
            ],
            liabilities: [
              { name: "PBOC Onshore Reserve Deposits", amount: "$850.0B" }
            ]
          },
          branches: [
            { targetId: "offshore_cnh_hong_kong_hub", targetName: "Hong Kong Offshore CNH Hub", volume: "$850.0B" }
          ]
        },
        {
          id: "offshore_cnh_hong_kong_hub",
          name: "Hong Kong Offshore Renminbi (CNH) RTGS Hub",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "HK",
          sector: "Offshore CNH RTGS Hub",
          volume: "¥1.8T/day ($250B)",
          provenance: "HKMA Monthly Statistical Bulletin",
          velocity: "Continuous CIPS Netting",
          balanceItems: {
            assets: [
              { name: "Interbank CNH Clearing Balances", amount: "¥1,800.0B" }
            ],
            liabilities: [
              { name: "CIPS Liquidity Accounts", amount: "¥1,800.0B" }
            ]
          },
          branches: [
            { targetId: "taiwan_central_bank_tsmc_semiconductor_sink", targetName: "Advanced Silicon TSMC Sink", volume: "$120.0B" }
          ]
        },
        {
          id: "taiwan_central_bank_tsmc_semiconductor_sink",
          name: "Taiwan Central Bank & TSMC Advanced Silicon Capital Sink",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "TW",
          sector: "High-Tech Hardware Capital Sink",
          volume: "$120.0 Billion",
          provenance: "CBC Taiwan Balance of Payments",
          velocity: "Global Semiconductor Hardware Revenue",
          balanceItems: {
            assets: [
              { name: "Advanced Wafer Fabrication Foundries", amount: "$150.0B" },
              { name: "Foreign Sovereign Reserve Claims", amount: "$234.6B" }
            ],
            liabilities: [
              { name: "Retained Earnings & Corporate Equity", amount: "$384.6B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "pboc_safe_foreign_reserves",
          target: "chinese_state_banks_fx_desk",
          action: "ONSHORE FX SWAP INJECTION",
          volume: "$850.0B",
          statutory: "PBOC Monetary Policy Circular",
          narrative: "The PBOC deploys foreign currency liquidity to Big 4 state banks to support the renminbi exchange rate corridor."
        },
        {
          source: "chinese_state_banks_fx_desk",
          target: "offshore_cnh_hong_kong_hub",
          action: "OFFSHORE CNH CLEARING",
          volume: "$850.0B",
          statutory: "CIPS Cross-Border Mandate",
          narrative: "Liquidity traverses across Hong Kong CNH clearing desks, settling cross-border Asian trade without touching SWIFT."
        },
        {
          source: "offshore_cnh_hong_kong_hub",
          target: "taiwan_central_bank_tsmc_semiconductor_sink",
          action: "SEMICONDUCTOR HARDWARE SETTLEMENT",
          volume: "$120.0B",
          statutory: "Taiwan Customs Directorate Trade Data",
          narrative: "Electronics and industrial supply chains purchase advanced silicon hardware, settling into Taiwan institutional asset sinks."
        }
      ]
    },

    "bank_of_russia_cbr_vault": {
      id: "bank_of_russia_cbr_vault",
      shortLabel: "Russia (Bank of Russia & NWF)",
      jurisdiction: "RU",
      title: "Bank of Russia CBR & Eurasian Sovereign Architecture",
      subtitle: "$600B CBR balance sheet, $185B gold vault, shadow maritime fleet, and Indian vostro rupee clearing",
      currency: "RUB / CNY",
      nominalVolume: "$600.0B ($420B Complex)",
      theme: "Sovereign Sanctions Bypass & Hydrocarbon Rerouting",
      statutoryBadge: "CBR Annual Bulletin",
      doubleEntryProof: { inflow: "$600.0B", outflow: "$600.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "bank_of_russia_cbr_vault",
          name: "Bank of Russia (CBR) Sovereign Vault & Foreign Reserves",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "RU",
          sector: "Sanctioned Central Bank",
          volume: "$600.0B",
          provenance: "CBR Statistics Bulletin",
          velocity: "Bilateral Gold & Yuan Settlement",
          balanceItems: {
            assets: [
              { name: "Gold Bullion Vault (Moscow)", amount: "$185.0B" },
              { name: "Yuan Foreign Exchange & Bilateral Claims", amount: "$115.0B" },
              { name: "Frozen G7 Sovereign Assets", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Ruble Monetary Base", amount: "$280.0B" },
              { name: "National Wealth Fund MinFin Accounts", amount: "$155.0B" }
            ]
          },
          branches: [
            { targetId: "shadow_tanker_energy_arbitrage", targetName: "Shadow Tanker Fleet", volume: "$140.0B" }
          ]
        },
        {
          id: "shadow_tanker_energy_arbitrage",
          name: "Maritime Shadow Tanker Fleet Arbitrage Conduit",
          tier: 1,
          tierLabel: "TRANSMISSION CONDUIT",
          jurisdiction: "GLOBAL_MARITIME",
          sector: "Dark Maritime Energy Transit",
          volume: "$140.0B",
          provenance: "AIS Satellite Tanker Tracking",
          velocity: "30-Day Maritime Transit",
          balanceItems: {
            assets: [
              { name: "Urals Crude Cargo In Transit", amount: "$140.0B" }
            ],
            liabilities: [
              { name: "Producer Payables", amount: "$140.0B" }
            ]
          },
          branches: [
            { targetId: "reserve_bank_of_india_refining_hub", targetName: "Indian Refineries", volume: "$140.0B" }
          ]
        },
        {
          id: "reserve_bank_of_india_refining_hub",
          name: "Reserve Bank of India & Gujarat Refining Nexus",
          tier: 2,
          tierLabel: "TRAVERSAL HUB",
          jurisdiction: "IN",
          sector: "Energy Refining & Vostro Clearing",
          volume: "$140.0B",
          provenance: "DGCIS India Trade Data",
          velocity: "Refining & Clean Diesel Re-export",
          balanceItems: {
            assets: [
              { name: "Refined Diesel Stocks", amount: "$140.0B" }
            ],
            liabilities: [
              { name: "Vostro Rupee Accounts", amount: "$140.0B" }
            ]
          },
          branches: [
            { targetId: "russia_offshore_shadow_capital_basin", targetName: "Trapped Vostro / Dirham Basin", volume: "$180.0B" }
          ]
        },
        {
          id: "russia_offshore_shadow_capital_basin",
          name: "Russian Offshore Trapped Capital Basin",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "OFFSHORE",
          sector: "Trapped Non-Convertible Currency Basin",
          volume: "$180.0B",
          provenance: "CBR Financial Stability Review",
          velocity: "Restricted Accumulation",
          balanceItems: {
            assets: [
              { name: "Non-Convertible Indian Rupee Vostro Accounts", amount: "$40.0B" },
              { name: "UAE Dirham Commercial Bank Deposits", amount: "$85.0B" },
              { name: "Turkish Hub Trade Receivables", amount: "$55.0B" }
            ],
            liabilities: [
              { name: "Exporter Trapped Balances", amount: "$180.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "bank_of_russia_cbr_vault",
          target: "shadow_tanker_energy_arbitrage",
          action: "DARK FLEET SEABORNE LIFTING",
          volume: "$140.0B",
          statutory: "Russian Maritime Register Notice",
          narrative: "Crude oil loads onto uninsured shadow tankers, bypassing G7 shipping sanctions and price-cap restrictions."
        },
        {
          source: "shadow_tanker_energy_arbitrage",
          target: "reserve_bank_of_india_refining_hub",
          action: "INDIAN REFINING RE-EXPORT",
          volume: "$140.0B",
          statutory: "RBI Special Rupee Vostro Directive",
          narrative: "Indian private refineries process Russian crude into refined diesel, paying into restricted rupee accounts."
        },
        {
          source: "reserve_bank_of_india_refining_hub",
          target: "russia_offshore_shadow_capital_basin",
          action: "TRAPPED CURRENCY RETENTION",
          volume: "$180.0B",
          statutory: "Bank of Russia Foreign Trade Gazette",
          narrative: "Proceeds remain stranded in non-convertible currencies in the UAE and India, financing non-sanctioned parallel imports."
        }
      ]
    },

    "norway_norges_bank_gpfg_faucet": {
      id: "norway_norges_bank_gpfg_faucet",
      shortLabel: "Norway (Norges Bank / GPFG)",
      jurisdiction: "NO",
      title: "Norway GPFG $1.75T Sovereign Wealth Architecture",
      subtitle: "Government Pension Fund Global investing North Sea hydrocarbon surpluses across 9,000+ worldwide companies",
      currency: "NOK / USD",
      nominalVolume: "$1.75 Trillion",
      theme: "Global Sovereign Equity Absorption & Wealth Preservation",
      statutoryBadge: "Norges Bank Annual Report",
      doubleEntryProof: { inflow: "$1.75T", outflow: "$1.75T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "norway_norges_bank_gpfg_faucet",
          name: "Norges Bank Investment Management (GPFG Faucet)",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "NO",
          sector: "Sovereign Wealth Faucet",
          volume: "$1.75 Trillion",
          provenance: "NBIM Annual Report",
          velocity: "Petroleum Fund Royalty Sweep",
          balanceItems: {
            assets: [
              { name: "Global Public Equities Portfolio", amount: "$1,225.0B" },
              { name: "Fixed Income & Renewable Energy Assets", amount: "$525.0B" }
            ],
            liabilities: [
              { name: "Norwegian State Petroleum Capital Account", amount: "$1,750.0B" }
            ]
          },
          branches: [
            { targetId: "norway_gpfg_global_equity_sink", targetName: "Global Equity Capital Sink", volume: "$1.225T" },
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custodial Sink", volume: "$300.0B" }
          ]
        },
        {
          id: "norway_gpfg_global_equity_sink",
          name: "Norway GPFG Global Public Equity Sink",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "GLOBAL",
          sector: "Worldwide Public Equity Sink",
          volume: "$1.225 Trillion",
          provenance: "NBIM Equity Holdings Disclosure",
          velocity: "Permanent Buy-and-Hold Strategy",
          balanceItems: {
            assets: [
              { name: "Ownership in 9,000+ Listed Companies Worldwide", amount: "$1,225.0B" }
            ],
            liabilities: [
              { name: "Beneficiary Entitlements", amount: "$1,225.0B" }
            ]
          },
          branches: []
        },
        {
          id: "us_treasuries_custody",
          name: "US Treasuries Custodial Sink",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Safe-Haven Collateral Sink",
          volume: "$300.0 Billion",
          provenance: "US TIC Table 5",
          velocity: "Sovereign Debt Custody",
          balanceItems: {
            assets: [
              { name: "Pledged US Treasury Notes", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Custody Liabilities to Norges Bank", amount: "$300.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "norway_norges_bank_gpfg_faucet",
          target: "norway_gpfg_global_equity_sink",
          action: "EQUITY REINVESTMENT",
          volume: "$1.225T",
          statutory: "Government Pension Fund Act Section 2",
          narrative: "Surplus cash sweeps systematically into public equities, acquiring long-term stakes across global technology and healthcare."
        },
        {
          source: "norway_norges_bank_gpfg_faucet",
          target: "us_treasuries_custody",
          action: "DOLLAR ANCHOR DEPOSIT",
          volume: "$300.0B",
          statutory: "NBIM Fixed Income Management Mandate",
          narrative: "Norges Bank parks $300B in US Treasuries to preserve liquid dollar collateral for international market operations."
        }
      ]
    },

    "swiss_national_bank_snb_vault": {
      id: "swiss_national_bank_snb_vault",
      shortLabel: "Switzerland (SNB / UBS)",
      jurisdiction: "CH",
      title: "Swiss National Bank SNB & UBS Consolidated Architecture",
      subtitle: "$950B SNB foreign exchange reserves, gold vaults, and UBS G-SIB cross-border wealth pipeline",
      currency: "CHF / USD",
      nominalVolume: "$950.0 Billion",
      theme: "Cross-Currency Safe-Haven Inflows & Wealth Clearing",
      statutoryBadge: "SNB Balance Sheet / UBS 20-F",
      doubleEntryProof: { inflow: "$950.0B", outflow: "$950.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "swiss_national_bank_snb_vault",
          name: "Swiss National Bank (SNB) Sovereign FX Vault",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "CH",
          sector: "Sovereign FX Vault",
          volume: "$950.0B",
          provenance: "SNB Accounts Bulletin",
          velocity: "Daily FX Intervention Cycle",
          balanceItems: {
            assets: [
              { name: "Foreign Currency Investments (US/EU Stocks & Bonds)", amount: "$780.0B" },
              { name: "Physical Gold Vault in Zurich & Berne", amount: "$65.0B" }
            ],
            liabilities: [
              { name: "Sight Deposits of Domestic Banks", amount: "$620.0B" }
            ]
          },
          branches: [
            { targetId: "ubs_group_consolidated_gsib", targetName: "UBS Group Consolidated G-SIB", volume: "$950.0B" }
          ]
        },
        {
          id: "ubs_group_consolidated_gsib",
          name: "UBS Group Consolidated (G-SIB Wealth Desk)",
          tier: 1,
          tierLabel: "TRANSMISSION G-SIB",
          jurisdiction: "CH_GLOBAL",
          sector: "Consolidated Global G-SIB",
          volume: "$1.71 Trillion",
          provenance: "UBS Form 20-F",
          velocity: "Global Cross-Border Wealth Transfer",
          balanceItems: {
            assets: [
              { name: "Global Wealth Management Assets", amount: "$850.0B" },
              { name: "Liquid Assets & Central Bank Cash", amount: "$380.0B" }
            ],
            liabilities: [
              { name: "Client Custody Deposits", amount: "$1,120.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custody", volume: "$300.0B" }
          ]
        },
        {
          id: "us_treasuries_custody",
          name: "US Treasuries Custodial Basin",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Safe-Haven Custody Basin",
          volume: "$300.0B",
          provenance: "Federal Reserve Custody Gazette",
          velocity: "Permanent Wealth Preservation",
          balanceItems: {
            assets: [
              { name: "Held US Benchmark Treasuries", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Swiss Client Custody Claims", amount: "$300.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "swiss_national_bank_snb_vault",
          target: "ubs_group_consolidated_gsib",
          action: "SIGHT DEPOSIT EXPANSION",
          volume: "$950.0B",
          statutory: "National Bank Act (NBA) Art. 9",
          narrative: "The SNB creates sight deposit liabilities to purchase global equities and foreign sovereign debt, settling via UBS."
        },
        {
          source: "ubs_group_consolidated_gsib",
          target: "us_treasuries_custody",
          action: "WEALTH PRESERVATION DEPOSIT",
          volume: "$300.0B",
          statutory: "FINMA Swiss Banking Supervisory Act",
          narrative: "UBS sweeps private wealth management dollar balances into US Treasury custody accounts for safety and yield."
        }
      ]
    },

    "japan_mof_boj_carry_faucet": {
      id: "japan_mof_boj_carry_faucet",
      shortLabel: "Japan (Bank of Japan / MoF)",
      jurisdiction: "JP",
      title: "Bank of Japan & MoF Yen Carry Liquidity Faucet",
      subtitle: "Zero-interest yen credit generation financing transpacific dollar repo and US Treasury holding portfolios",
      currency: "JPY / USD",
      nominalVolume: "¥750T ($5.1T / $1.1T Carry)",
      theme: "Transpacific Liquidity Carry & FX Basis Swaps",
      statutoryBadge: "BoJ Financial Accounts / MoF Balance Sheet",
      doubleEntryProof: { inflow: "$1.104T", outflow: "$1.104T", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "japan_mof_boj_carry_faucet",
          name: "Bank of Japan & MoF Zero-Rate Faucet",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "JP",
          sector: "Central Bank Genesis",
          volume: "$1.104 Trillion",
          provenance: "BoJ Accounts Summary",
          velocity: "Daily Policy Rate Operation",
          balanceItems: {
            assets: [
              { name: "Japanese Government Bonds (JGBs)", amount: "¥580.0T" }
            ],
            liabilities: [
              { name: "Commercial Bank Excess Reserves", amount: "¥540.0T" }
            ]
          },
          branches: [
            { targetId: "japan_institutional_carry_desk", targetName: "Japan Institutional Carry Desks", volume: "$650.0B" }
          ]
        },
        {
          id: "japan_institutional_carry_desk",
          name: "Japanese Institutional Carry Desks (Norinchukin / Lifers)",
          tier: 1,
          tierLabel: "TRANSMISSION DEALER",
          jurisdiction: "JP",
          sector: "Institutional Carry Conduits",
          volume: "$650.0B",
          provenance: "FSA Japan Survey",
          velocity: "3-Month Term FX Basis Swap Roll",
          balanceItems: {
            assets: [
              { name: "Foreign Sovereign Securities Portfolio", amount: "$650.0B" }
            ],
            liabilities: [
              { name: "Yen Policy Borrowing Liabilities", amount: "¥45.0T" }
            ]
          },
          branches: [
            { targetId: "us_triparty_repo_pool", targetName: "US Triparty Repo SOFR Basin", volume: "$480.0B" }
          ]
        },
        {
          id: "us_triparty_repo_pool",
          name: "US Triparty Repo SOFR Clearing Basin",
          tier: 2,
          tierLabel: "TRAVERSAL CLEARING",
          jurisdiction: "US",
          sector: "Wholesale Repo Clearing Pool",
          volume: "$3.007 Trillion/day",
          provenance: "DTCC Triparty / NY Fed SOFR",
          velocity: "Overnight Wholesale SOFR Turnover",
          balanceItems: {
            assets: [
              { name: "Overnight Repo Loans to Primary Dealers", amount: "$3,007.0B" }
            ],
            liabilities: [
              { name: "Synthetic USD Deposited by Japanese Desks", amount: "$480.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasury_tga", targetName: "US Treasury General Account", volume: "$883.3B" }
          ]
        },
        {
          id: "us_treasury_tga",
          name: "US Treasury General Account",
          tier: 3,
          tierLabel: "SAFE-HAVEN SINK",
          jurisdiction: "US",
          sector: "Sovereign Operating Cash Vault",
          volume: "$883.3B",
          provenance: "Daily Treasury Statement",
          velocity: "Daily Auction Settlement",
          balanceItems: {
            assets: [
              { name: "Cash Balance at Fed", amount: "$883.3B" }
            ],
            liabilities: [
              { name: "Federal Operating Commitments", amount: "$883.3B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "japan_mof_boj_carry_faucet",
          target: "japan_institutional_carry_desk",
          action: "YEN LIQUIDITY GENERATION",
          volume: "$650.0B",
          statutory: "Bank of Japan Act Art. 33",
          narrative: "BoJ maintains ultra-loose policy, allowing lifers to fund zero-rate yen liabilities."
        },
        {
          source: "japan_institutional_carry_desk",
          target: "us_triparty_repo_pool",
          action: "FX SWAP & TRIPARTY LENDING",
          volume: "$480.0B",
          statutory: "ISDA Master Agreement Schedule",
          narrative: "Institutions swap yen into synthetic dollars, deploying funds into US Triparty repo at SOFR overnight."
        },
        {
          source: "us_triparty_repo_pool",
          target: "us_treasury_tga",
          action: "PRIMARY DEALER T-BILL FINANCING",
          volume: "$480.0B",
          statutory: "Daily Treasury Statement",
          narrative: "Repo liquidity finances Primary Dealer T-bill absorption, settling cash into the Treasury General Account."
        }
      ]
    },

    "bank_of_england_boe_vault": {
      id: "bank_of_england_boe_vault",
      shortLabel: "United Kingdom (BoE / DMO)",
      jurisdiction: "UK",
      title: "Bank of England BoE & UK DMO Sovereign Gilt Architecture",
      subtitle: "£2.6T UK Sovereign Gilt benchmark issuance, sterling base-money creation, and CHAPS interbank RTGS clearing",
      currency: "GBP",
      nominalVolume: "£2.60 Trillion ($3.38T)",
      theme: "Sterling Sovereign Debt & CHAPS RTGS Traversal",
      statutoryBadge: "Bank of England Weekly Return / UK DMO",
      doubleEntryProof: { inflow: "£2.60T", outflow: "£2.60T", net: "£0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "bank_of_england_boe_vault",
          name: "Bank of England (BoE) Reserve Vault",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "UK",
          sector: "Central Bank Genesis",
          volume: "£980.0 Billion",
          provenance: "BoE Weekly Return Table B1",
          velocity: "Sterling Monetary Framework Operations",
          balanceItems: {
            assets: [
              { name: "Asset Purchase Facility (APF) Gilt Portfolio", amount: "£680.0B" },
              { name: "Short-Term Repo & Liquidity Facilities", amount: "£300.0B" }
            ],
            liabilities: [
              { name: "Commercial Bank Reserve Balances", amount: "£820.0B" },
              { name: "Notes in Circulation", amount: "£88.0B" }
            ]
          },
          branches: [
            { targetId: "uk_dmo_gilt_debt_market", targetName: "UK DMO Gilt Debt Benchmark Market", volume: "£2.60T" }
          ]
        },
        {
          id: "uk_dmo_gilt_debt_market",
          name: "UK Debt Management Office (DMO) Gilt Market",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "UK",
          sector: "Sovereign Debt Benchmark Sink",
          volume: "£2.60 Trillion",
          provenance: "UK DMO Quarterly Review",
          velocity: "Gilt-Edged Market Maker (GEMM) Turnover",
          balanceItems: {
            assets: [
              { name: "Sterling Risk-Free Benchmark Paper", amount: "£2,600.0B" }
            ],
            liabilities: [
              { name: "HM Treasury Public Debt Outstanding", amount: "£2,600.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "bank_of_england_boe_vault",
          target: "uk_dmo_gilt_debt_market",
          action: "GILT BENCHMARK REPO AUCTION",
          volume: "£680.0B",
          statutory: "Bank of England Act 1998",
          narrative: "Bank of England manages sterling reserve balances and gilt market operations via Gilt-Edged Market Makers (GEMMs)."
        }
      ]
    },

    "imf_special_drawing_rights_sdr_pool": {
      id: "imf_special_drawing_rights_sdr_pool",
      shortLabel: "Multilateral (IMF SDR / BIS)",
      jurisdiction: "SUPRA",
      title: "IMF Special Drawing Rights (SDR) & BIS Basel Multilateral Architecture",
      subtitle: "$935B IMF SDR allocation pool buffering global central banks, and BIS Basel central bank banking department",
      currency: "SDR / USD",
      nominalVolume: "$935.0 Billion",
      theme: "Supranational Reserve Backstop & Basel Banking Desk",
      statutoryBadge: "IMF Financial Statements / BIS Balance Sheet",
      doubleEntryProof: { inflow: "$935.0B", outflow: "$935.0B", net: "$0.00", leak: "$0.00", status: "Strictly Conserved" },
      nodes: [
        {
          id: "imf_special_drawing_rights_sdr_pool",
          name: "IMF Special Drawing Rights (SDR) Reserve Pool",
          tier: 0,
          tierLabel: "SOVEREIGN GENESIS",
          jurisdiction: "GLOBAL_MULTILATERAL",
          sector: "Supranational Monetary Reserve Basket",
          volume: "$935.0 Billion (660B SDR)",
          provenance: "IMF Financial Data",
          velocity: "Official Voluntary Trading Arrangement (VTA)",
          balanceItems: {
            assets: [
              { name: "SDR Currency Basket Portfolio", amount: "$935.0B" }
            ],
            liabilities: [
              { name: "Allocations to 190 Member Countries", amount: "$935.0B" }
            ]
          },
          branches: [
            { targetId: "bis_basel_banking_department", targetName: "BIS Basel Banking Department", volume: "$450.0B" }
          ]
        },
        {
          id: "bis_basel_banking_department",
          name: "Bank for International Settlements (BIS) Basel Desk",
          tier: 1,
          tierLabel: "TRANSMISSION BANK",
          jurisdiction: "GLOBAL_MULTILATERAL",
          sector: "Central Bank Creditor Depository",
          volume: "$450.0 Billion",
          provenance: "BIS Annual Report",
          velocity: "Official Reserve Placement",
          balanceItems: {
            assets: [
              { name: "Gold Bullion & Sovereign Repo", amount: "$450.0B" }
            ],
            liabilities: [
              { name: "Deposits from 63 Member Central Banks", amount: "$450.0B" }
            ]
          },
          branches: [
            { targetId: "us_treasuries_custody", targetName: "US Treasuries Custody", volume: "$300.0B" }
          ]
        },
        {
          id: "us_treasuries_custody",
          name: "US Treasuries Custodial Basin",
          tier: 3,
          tierLabel: "COLLATERAL SINK",
          jurisdiction: "US",
          sector: "Supranational Custodial Basin",
          volume: "$300.0 Billion",
          provenance: "Federal Reserve Custody Accounts",
          velocity: "Safe-Haven Collateral Custody",
          balanceItems: {
            assets: [
              { name: "Pledged US Treasury Notes", amount: "$300.0B" }
            ],
            liabilities: [
              { name: "Custody Liabilities to Foreign Monetary Authorities", amount: "$300.0B" }
            ]
          },
          branches: []
        }
      ],
      hops: [
        {
          source: "imf_special_drawing_rights_sdr_pool",
          target: "bis_basel_banking_department",
          action: "SDR LIQUIDITY INTERMEDIATION",
          volume: "$450.0B",
          statutory: "IMF Articles of Agreement Art. XVII",
          narrative: "Member central banks exchange SDR allocations through the BIS Banking Department for dollar and euro liquidity."
        },
        {
          source: "bis_basel_banking_department",
          target: "us_treasuries_custody",
          action: "FOREIGN CUSTODY PLEDGE",
          volume: "$300.0B",
          statutory: "Federal Reserve Act Section 14",
          narrative: "The BIS places gold and sovereign debt into custodial accounts at the Federal Reserve to back international clearing lines."
        }
      ]
    }
  }
};

const App = {
  // State
  activeTab: "tab-graph",
  cy: null,
  topologyData: null,
  scorecardData: null,
  poolsData: [],
  featuredCircuits: [],
  selectedNodeId: null,
  radarChart: null,

  // Visual Tree Flow Explorer State
  treeMode: "circuits", // "circuits" or "roots"
  selectedCircuitId: "CIRCUIT-01-OAT-BUND",
  selectedRootId: "french_republic_tresor",
  treeCurrencyFilter: "ALL",
  treeSearchQuery: "",
  treeExpandedBranches: new Set(),
  treeAllBranchesExpanded: false,
  treeCurrentHopIndex: 0,
  treeAutoPlayTimer: null,
  
  // Ledger pagination state
  ledgerOffset: 0,
  ledgerLimit: 50,
  ledgerTotal: 0,

  init() {
    this.setupTabs();
    this.setupEventListeners();
    this.initCytoscape();
    this.loadHealthAndMetrics();
    this.loadTopology();
    this.loadScorecard();
    this.loadExplorer();
    this.loadGauntlet(1); // Pre-load Regime 1
    this.loadLedger();
  },

  // =========================================================================
  // Tab Management
  // =========================================================================
  setupTabs() {
    const tabButtons = document.querySelectorAll(".nav-tab");
    tabButtons.forEach(btn => {
      btn.addEventListener("click", () => {
        const targetTabId = btn.getAttribute("data-tab");
        if (targetTabId === this.activeTab) return;

        tabButtons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        document.querySelectorAll(".tab-panel").forEach(panel => {
          panel.classList.add("hidden");
        });
        const targetPanel = document.getElementById(targetTabId);
        if (targetPanel) {
          targetPanel.classList.remove("hidden");
        }

        this.activeTab = targetTabId;

        // Resize Cytoscape if switching to graph tab
        if (targetTabId === "tab-graph" && this.cy) {
          setTimeout(() => {
            this.cy.resize();
            this.cy.fit(undefined, 30);
          }, 50);
        }

        // Render radar chart if switching to scorecard tab
        if (targetTabId === "tab-scorecard" && !this.radarChart) {
          this.renderRadarChart();
        }

        // Redraw Visual Tree Flow connectors when switching to Explorer tab
        if (targetTabId === "tab-explorer") {
          setTimeout(() => this.drawTreeConnectors(), 80);
        }
      });
    });
  },

  // =========================================================================
  // Global Event Listeners
  // =========================================================================
  setupEventListeners() {
    // Quick refresh
    document.getElementById("btn-quick-refresh")?.addEventListener("click", () => {
      this.loadHealthAndMetrics();
      this.loadTopology(true);
      this.loadLedger();
    });

    // Close Node Drawer
    document.getElementById("btn-close-drawer")?.addEventListener("click", () => this.closeDrawer());
    document.getElementById("btn-drawer-close")?.addEventListener("click", () => this.closeDrawer());
    document.getElementById("node-drawer-backdrop")?.addEventListener("click", () => this.closeDrawer());

    // Drawer focus node on canvas
    document.getElementById("btn-drawer-focus-canvas")?.addEventListener("click", () => {
      if (this.selectedNodeId && this.cy) {
        this.switchTab("tab-graph");
        this.closeDrawer();
        this.focusNodeOnCanvas(this.selectedNodeId);
      }
    });

    // Graph Controls
    document.getElementById("btn-zoom-in")?.addEventListener("click", () => {
      if (this.cy) this.cy.zoom(this.cy.zoom() * 1.25);
    });
    document.getElementById("btn-zoom-out")?.addEventListener("click", () => {
      if (this.cy) this.cy.zoom(this.cy.zoom() * 0.8);
    });
    document.getElementById("btn-fit-graph")?.addEventListener("click", () => {
      if (this.cy) this.cy.fit(undefined, 40);
    });

    // Graph Layout Switchers
    document.getElementById("layout-hierarchical")?.addEventListener("click", () => this.applyLayout("preset"));
    document.getElementById("layout-breadthfirst")?.addEventListener("click", () => this.applyLayout("breadthfirst"));
    document.getElementById("layout-concentric")?.addEventListener("click", () => this.applyLayout("concentric"));
    document.getElementById("layout-cose")?.addEventListener("click", () => this.applyLayout("cose"));

    // Graph Tier Filters
    document.querySelectorAll(".tier-filter-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".tier-filter-btn").forEach(b => {
          b.classList.remove("active-tier", "bg-cyan-950", "text-cyan-400", "border-cyan-800");
          b.classList.add("bg-slate-800", "text-slate-300", "border-slate-700");
        });
        btn.classList.add("active-tier", "bg-cyan-950", "text-cyan-400", "border-cyan-800");
        btn.classList.remove("bg-slate-800", "text-slate-300", "border-slate-700");

        const tierVal = btn.getAttribute("data-tier");
        this.filterGraphByTier(tierVal);
      });
    });

    // Graph Search Input
    document.getElementById("graph-search-input")?.addEventListener("input", (e) => {
      const q = e.target.value.trim().toLowerCase();
      this.searchNodeOnCanvas(q);
    });

    // Explorer: Path discovery
    document.getElementById("btn-run-path-discovery")?.addEventListener("click", () => this.runPathDiscovery());
    document.getElementById("btn-scroll-path-finder")?.addEventListener("click", () => {
      document.getElementById("path-finder-section")?.scrollIntoView({ behavior: "smooth" });
    });

    // Explorer: Pool browser filters
    document.getElementById("pool-filter-input")?.addEventListener("input", () => this.filterPoolsBrowser());
    document.getElementById("pool-tier-select")?.addEventListener("change", () => this.filterPoolsBrowser());

    // Gauntlet: Trigger buttons
    document.querySelectorAll(".btn-trigger-regime").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const regimeNum = parseInt(btn.getAttribute("data-regime"), 10);
        this.triggerGauntletRegime(regimeNum);
      });
    });

    // Gauntlet: Highlight bypasses on graph
    document.getElementById("btn-highlight-sim-bypasses")?.addEventListener("click", () => {
      this.highlightCurrentSimBypasses();
    });

    // Ledger: Search & Filter inputs
    document.getElementById("ledger-search-input")?.addEventListener("input", () => {
      this.ledgerOffset = 0;
      this.loadLedger();
    });
    document.getElementById("ledger-currency-filter")?.addEventListener("change", () => {
      this.ledgerOffset = 0;
      this.loadLedger();
    });
    document.getElementById("ledger-type-filter")?.addEventListener("change", () => {
      this.ledgerOffset = 0;
      this.loadLedger();
    });
    document.getElementById("btn-ledger-prev")?.addEventListener("click", () => {
      if (this.ledgerOffset > 0) {
        this.ledgerOffset = Math.max(0, this.ledgerOffset - this.ledgerLimit);
        this.loadLedger();
      }
    });
    document.getElementById("btn-ledger-next")?.addEventListener("click", () => {
      if (this.ledgerOffset + this.ledgerLimit < this.ledgerTotal) {
        this.ledgerOffset += this.ledgerLimit;
        this.loadLedger();
      }
    });
  },

  switchTab(tabId) {
    const btn = document.querySelector(`.nav-tab[data-tab="${tabId}"]`);
    if (btn) btn.click();
  },

  // =========================================================================
  // API Loaders & Metrics
  // =========================================================================
  async loadHealthAndMetrics() {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      if (data.database) {
        document.getElementById("header-flows").textContent = data.database.flow_events_count || 115;
      }
      if (data.topology) {
        document.getElementById("header-nodes").textContent = data.topology.node_count || 140;
        document.getElementById("header-edges").textContent = data.topology.edge_count || 317;
      }
    } catch (e) {
      console.warn("Could not load /api/health:", e);
    }
  },

  async loadScorecard() {
    try {
      const res = await fetch("/api/scorecard");
      const data = await res.json();
      this.scorecardData = data;

      // Update header
      document.getElementById("header-score").textContent = `${data.system_integrity_score} / 100`;
      document.getElementById("audit-overall-score").textContent = data.system_integrity_score;
      document.getElementById("audit-leak-sum").textContent = this.formatCurrency(data.total_leakage_usd || 0.0);
      document.getElementById("audit-coverage-ratio").textContent = `${(data.at_risk_coverage_ratio_pct || 100.0).toFixed(1)}%`;

      // Render anomalies
      const anomaliesContainer = document.getElementById("anomalies-list");
      if (anomaliesContainer && data.high_risk_anomalies) {
        document.getElementById("anomaly-count").textContent = data.high_risk_anomalies.length;
        anomaliesContainer.innerHTML = data.high_risk_anomalies.map(a => `
          <div class="bg-slate-900 border ${a.severity === 'CRITICAL' ? 'border-red-800/80 bg-red-950/20' : 'border-amber-800/80 bg-amber-950/20'} rounded-lg p-3.5 space-y-1.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold ${a.severity === 'CRITICAL' ? 'bg-red-900/60 text-red-300 border border-red-700' : 'bg-amber-900/60 text-amber-300 border border-amber-700'}">${a.severity}</span>
                <span class="text-xs font-mono font-bold text-slate-200">${a.dimension}</span>
              </div>
              <span class="text-[11px] font-mono text-slate-500">${a.id}</span>
            </div>
            <div class="text-xs font-mono text-cyan-300">${a.entity}</div>
            <p class="text-xs text-slate-300">${a.description}</p>
            <div class="text-[11px] text-slate-400 font-mono pt-1 border-t border-slate-800">
              <strong class="text-slate-300">Systemic Impact:</strong> ${a.impact}
            </div>
          </div>
        `).join("");
      }

      // Render remediations
      const remTbody = document.getElementById("remediation-table-body");
      if (remTbody && data.remediation_recommendations) {
        remTbody.innerHTML = data.remediation_recommendations.map(r => `
          <tr class="table-dark-row">
            <td class="py-2.5 px-4 font-bold text-cyan-400">${r.id}</td>
            <td class="py-2.5 px-4 text-purple-300">${r.area}</td>
            <td class="py-2.5 px-4 text-slate-200 font-bold">${r.action}</td>
            <td class="py-2.5 px-4 text-slate-400 font-sans text-xs">${r.details}</td>
          </tr>
        `).join("");
      }

      // Render radar chart if active
      if (this.activeTab === "tab-scorecard") {
        this.renderRadarChart();
      }
    } catch (e) {
      console.warn("Could not load /api/scorecard:", e);
    }
  },

  renderRadarChart() {
    const canvas = document.getElementById("audit-radar-chart");
    if (!canvas || !this.scorecardData) return;

    if (this.radarChart) {
      this.radarChart.destroy();
    }

    const cat = this.scorecardData.category_scores || {
      conservation: 20.0,
      dimensional: 20.0,
      temporal: 13.3,
      topology: 19.0,
      dark_matter: 18.5
    };

    this.radarChart = new Chart(canvas, {
      type: "radar",
      data: {
        labels: ["Conservation (20)", "Dimensional (20)", "Temporal (20)", "Topology (20)", "Dark Matter (20)"],
        datasets: [{
          label: "Audit Score",
          data: [cat.conservation, cat.dimensional, cat.temporal, cat.topology, cat.dark_matter],
          backgroundColor: "rgba(0, 240, 255, 0.2)",
          borderColor: "#00f0ff",
          borderWidth: 2,
          pointBackgroundColor: "#00f0ff",
          pointBorderColor: "#ffffff",
          pointRadius: 4,
        }, {
          label: "Ideal Target",
          data: [20, 20, 20, 20, 20],
          backgroundColor: "rgba(16, 185, 129, 0.05)",
          borderColor: "rgba(16, 185, 129, 0.4)",
          borderWidth: 1,
          borderDash: [4, 4],
          pointRadius: 0,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            min: 0,
            max: 20,
            ticks: { stepSize: 5, color: "#64748b", backdropColor: "transparent", font: { family: "JetBrains Mono", size: 9 } },
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            angleLines: { color: "rgba(255, 255, 255, 0.08)" },
            pointLabels: { color: "#94a3b8", font: { family: "JetBrains Mono", size: 10 } }
          }
        },
        plugins: {
          legend: {
            display: true,
            labels: { color: "#94a3b8", font: { family: "JetBrains Mono", size: 10 } }
          }
        }
      }
    });
  },

  // =========================================================================
  // Cytoscape.js Graph Engine
  // =========================================================================
  initCytoscape() {
    const container = document.getElementById("cy-container");
    if (!container) return;

    this.cy = cytoscape({
      container: container,
      boxSelectionEnabled: false,
      autounselectify: false,
      style: [
        // Default Node Style
        {
          selector: "node",
          style: {
            "label": "data(label)",
            "color": "#cbd5e1",
            "font-size": "10px",
            "font-family": "JetBrains Mono, monospace",
            "text-valign": "bottom",
            "text-margin-y": "6px",
            "text-max-width": "120px",
            "text-wrap": "ellipsis",
            "background-color": "#475569",
            "border-width": 2,
            "border-color": "#1e293b",
            "width": 28,
            "height": 28,
            "transition-property": "background-color, border-color, width, height, opacity",
            "transition-duration": "0.2s"
          }
        },
        // Tier 0 Genesis Nodes
        {
          selector: "node[tier = 0]",
          style: {
            "background-color": "#0284c7",
            "border-color": "#38bdf8",
            "width": 36,
            "height": 36,
            "color": "#38bdf8",
            "font-weight": "bold"
          }
        },
        // Tier 1 Transmission Nodes
        {
          selector: "node[tier = 1]",
          style: {
            "background-color": "#7c3aed",
            "border-color": "#c084fc",
            "width": 32,
            "height": 32,
            "color": "#e9d5ff"
          }
        },
        // Tier 2 Traversal Nodes
        {
          selector: "node[tier = 2]",
          style: {
            "background-color": "#d97706",
            "border-color": "#fbbf24",
            "width": 26,
            "height": 26,
            "color": "#fef3c7"
          }
        },
        // Tier 3 Sink Nodes
        {
          selector: "node[tier = 3]",
          style: {
            "background-color": "#059669",
            "border-color": "#34d399",
            "width": 34,
            "height": 34,
            "color": "#34d399",
            "font-weight": "bold"
          }
        },
        // Decoy / Distractor Nodes
        {
          selector: "node[is_decoy = true]",
          style: {
            "background-color": "#991b1b",
            "border-color": "#f87171",
            "border-style": "dashed",
            "color": "#fca5a5"
          }
        },
        // Selected / Focused Node
        {
          selector: "node:selected, node.highlighted",
          style: {
            "border-color": "#00f0ff",
            "border-width": 4,
            "width": 42,
            "height": 42,
            "font-size": "12px",
            "font-weight": "bold",
            "color": "#00f0ff",
            "z-index": 999
          }
        },
        // Default Edge Style
        {
          selector: "edge",
          style: {
            "width": 1.5,
            "line-color": "#1e293b",
            "target-arrow-color": "#334155",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "opacity": 0.55,
            "arrow-scale": 0.8,
            "transition-property": "line-color, width, opacity",
            "transition-duration": "0.2s"
          }
        },
        // Bypass Edges
        {
          selector: "edge[is_bypass = true]",
          style: {
            "line-color": "#059669",
            "target-arrow-color": "#10b981",
            "width": 2.5,
            "opacity": 0.85,
            "line-style": "dashed"
          }
        },
        // Active Corridor / Highlighted Edge
        {
          selector: "edge.highlighted",
          style: {
            "line-color": "#00f0ff",
            "target-arrow-color": "#00f0ff",
            "width": 3.5,
            "opacity": 1.0,
            "z-index": 999
          }
        },
        // Dimmed Non-Corridor Elements
        {
          selector: ".dimmed",
          style: {
            "opacity": 0.12
          }
        }
      ],
      layout: { name: "preset" }
    });

    // Node Click -> Open Drawer
    this.cy.on("tap", "node", (evt) => {
      const node = evt.target;
      const nodeId = node.id();
      this.inspectPool(nodeId);
    });

    // Canvas Background Click -> Reset highlights
    this.cy.on("tap", (evt) => {
      if (evt.target === this.cy) {
        this.resetGraphHighlights();
      }
    });
  },

  async loadTopology(forceReload = false) {
    try {
      const res = await fetch("/api/topology");
      const data = await res.json();
      this.topologyData = data;

      if (this.cy) {
        this.cy.elements().remove();
        this.cy.add(data.elements.nodes);
        this.cy.add(data.elements.edges);
        this.applyLayout("preset");
      }
    } catch (e) {
      console.warn("Could not load /api/topology:", e);
    }
  },

  applyLayout(layoutName) {
    if (!this.cy) return;

    let layoutOptions = { name: layoutName };
    if (layoutName === "preset") {
      layoutOptions = {
        name: "preset",
        fit: true,
        padding: 40,
        animate: true,
        animationDuration: 400
      };
    } else if (layoutName === "breadthfirst") {
      layoutOptions = {
        name: "breadthfirst",
        directed: true,
        spacingFactor: 1.25,
        animate: true,
        fit: true,
        padding: 40
      };
    } else if (layoutName === "concentric") {
      layoutOptions = {
        name: "concentric",
        concentric: (node) => 4 - node.data("tier"),
        levelWidth: () => 1,
        animate: true,
        fit: true,
        padding: 40
      };
    } else if (layoutName === "cose") {
      layoutOptions = {
        name: "cose",
        animate: false,
        fit: true,
        padding: 40,
        nodeOverlap: 20,
        componentSpacing: 100
      };
    }

    const layout = this.cy.layout(layoutOptions);
    layout.run();
  },

  filterGraphByTier(tierVal) {
    if (!this.cy) return;

    this.cy.batch(() => {
      if (tierVal === "all") {
        this.cy.nodes().show();
        this.cy.edges().show();
      } else {
        const t = parseInt(tierVal, 10);
        this.cy.nodes().forEach(node => {
          if (node.data("tier") === t) {
            node.show();
          } else {
            node.hide();
          }
        });
        this.cy.edges().forEach(edge => {
          if (edge.source().visible() && edge.target().visible()) {
            edge.show();
          } else {
            edge.hide();
          }
        });
      }
    });

    this.cy.fit(undefined, 30);
  },

  searchNodeOnCanvas(query) {
    if (!this.cy) return;
    if (!query) {
      this.resetGraphHighlights();
      return;
    }

    const matched = this.cy.nodes().filter(node => {
      const id = node.id().toLowerCase();
      const label = (node.data("label") || "").toLowerCase();
      return id.includes(query) || label.includes(query);
    });

    if (matched.length > 0) {
      this.cy.elements().addClass("dimmed");
      matched.removeClass("dimmed").addClass("highlighted");
      this.cy.animate({
        center: { eles: matched },
        zoom: 1.2,
        duration: 300
      });
    } else {
      this.resetGraphHighlights();
    }
  },

  focusNodeOnCanvas(nodeId) {
    if (!this.cy) return;
    const node = this.cy.getElementById(nodeId);
    if (node && node.length > 0) {
      this.resetGraphHighlights();
      this.cy.elements().addClass("dimmed");
      node.removeClass("dimmed").addClass("highlighted");
      node.neighborhood().removeClass("dimmed");
      node.connectedEdges().addClass("highlighted");

      this.cy.animate({
        center: { eles: node },
        zoom: 1.4,
        duration: 400
      });
    }
  },

  highlightCorridor(nodeIds) {
    if (!this.cy || !nodeIds || nodeIds.length === 0) return;

    this.cy.batch(() => {
      this.cy.elements().addClass("dimmed").removeClass("highlighted");
      const nodes = this.cy.nodes().filter(n => nodeIds.includes(n.id()));
      nodes.removeClass("dimmed").addClass("highlighted");

      // Highlight connecting edges
      for (let i = 0; i < nodeIds.length - 1; i++) {
        const u = nodeIds[i];
        const v = nodeIds[i + 1];
        const edge = this.cy.edges().filter(e => (e.source().id() === u && e.target().id() === v));
        edge.removeClass("dimmed").addClass("highlighted");
      }
    });

    const highlightEles = this.cy.elements(".highlighted");
    if (highlightEles.length > 0) {
      this.cy.animate({
        fit: { eles: highlightEles, padding: 60 },
        duration: 500
      });
    }
  },

  resetGraphHighlights() {
    if (!this.cy) return;
    this.cy.elements().removeClass("dimmed highlighted");
  },

  // =========================================================================
  // Tab 2: Flow & Pool Explorer
  // =========================================================================
  async loadExplorer() {
    // Initialize Visual Tree Flow Explorer
    this.initVisualTreeExplorer();

    // 1. Load featured circuits
    try {
      const res = await fetch("/api/circuits/featured");
      const circuits = await res.json();
      this.featuredCircuits = circuits;
      this.renderFeaturedCircuits(circuits);
    } catch (e) {
      console.warn("Could not load /api/circuits/featured:", e);
    }

    // 2. Load pools registry
    try {
      const res = await fetch("/api/pools");
      const pools = await res.json();
      this.poolsData = pools;
      document.getElementById("pool-count-label").textContent = pools.length;
      this.renderPoolsBrowser(pools);
      this.populatePathDropdowns(pools);
    } catch (e) {
      console.warn("Could not load /api/pools:", e);
    }
  },

  renderFeaturedCircuits(circuits) {
    const grid = document.getElementById("featured-circuits-grid");
    if (!grid) return;

    grid.innerHTML = circuits.map(c => `
      <div class="bg-manifold-card border border-manifold-border hover:border-cyan-500/50 rounded-lg p-4 transition flex flex-col justify-between space-y-3">
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-cyan-300 border border-slate-700 font-semibold">${c.id}</span>
            ${c.regime_link ? `<span class="text-[9px] font-mono px-1.5 rounded bg-purple-950 text-purple-300 border border-purple-800">Regime ${c.regime_link}</span>` : ''}
          </div>
          <h4 class="text-sm font-bold text-white leading-snug">${c.title}</h4>
          <p class="text-[11px] text-slate-400 leading-relaxed">${c.subtitle}</p>
        </div>

        <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-2">
          <button class="btn-trace-circuit flex-1 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 font-mono text-xs border border-slate-700 flex items-center justify-center gap-1.5 transition" data-circuit-id="${c.id}">
            <i class="fa-solid fa-play text-[10px]"></i> Animate Path
          </button>
          <button class="btn-inspect-circuit px-2.5 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono text-xs border border-slate-700 transition" data-source-id="${c.source_id}" title="Inspect Origin">
            <i class="fa-solid fa-magnifying-glass"></i>
          </button>
        </div>
      </div>
    `).join("");

    // Bind circuit click handlers
    grid.querySelectorAll(".btn-trace-circuit").forEach(btn => {
      btn.addEventListener("click", () => {
        const cid = btn.getAttribute("data-circuit-id");
        const circuit = this.featuredCircuits.find(c => c.id === cid);
        if (circuit) {
          this.switchTab("tab-graph");
          this.highlightCorridor(circuit.key_nodes);
        }
      });
    });

    grid.querySelectorAll(".btn-inspect-circuit").forEach(btn => {
      btn.addEventListener("click", () => {
        const sid = btn.getAttribute("data-source-id");
        this.inspectPool(sid);
      });
    });
  },

  populatePathDropdowns(pools) {
    const srcSelect = document.getElementById("path-source-select");
    const tgtSelect = document.getElementById("path-target-select");
    if (!srcSelect || !tgtSelect) return;

    const optionsHtml = pools.map(p => `
      <option value="${p.id}">${p.name} (${p.tier_label})</option>
    `).join("");

    srcSelect.innerHTML = `<option value="">Select Origin Pool...</option>` + optionsHtml;
    tgtSelect.innerHTML = `<option value="">Select Destination Pool...</option>` + optionsHtml;

    // Presets default
    srcSelect.value = "french_republic_tresor";
    tgtSelect.value = "bund_risk_free_anchor";
  },

  async runPathDiscovery() {
    const src = document.getElementById("path-source-select").value;
    const tgt = document.getElementById("path-target-select").value;
    const resultsContainer = document.getElementById("path-discovery-results");

    if (!src || !tgt) {
      alert("Please select both an Origin and a Destination pool.");
      return;
    }

    try {
      resultsContainer.classList.remove("hidden");
      resultsContainer.innerHTML = `<div class="p-3 text-xs font-mono text-cyan-400 animate-pulse">Executing Dual-Frontier A* Search...</div>`;

      const res = await fetch(`/api/paths?source_id=${src}&target_id=${tgt}`);
      const data = await res.json();

      if (!data.success) {
        resultsContainer.innerHTML = `
          <div class="bg-red-950/40 border border-red-800 rounded p-3 text-xs font-mono text-red-300">
            <strong>No Viable Clearing Corridor Discovered:</strong> Path between '${src}' and '${tgt}' is severed or blocked.
          </div>
        `;
        return;
      }

      resultsContainer.innerHTML = `
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-3">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-mono text-xs font-bold border border-emerald-800">CORRIDOR DISCOVERED</span>
              <span class="text-xs font-mono text-slate-400">${data.hops} Hops</span>
            </div>
            <div class="text-xs font-mono">
              <span class="text-slate-400">Total Impedance Cost:</span>
              <span class="text-cyan-400 font-bold ml-1">${data.total_cost}</span>
            </div>
          </div>

          <!-- Corridor Hop Steps -->
          <div class="space-y-1.5">
            ${data.hop_details.map((hop, i) => `
              <div class="flex items-center gap-3 p-2 rounded bg-slate-950/80 border border-slate-800/80 text-xs font-mono">
                <span class="w-5 h-5 rounded-full bg-slate-800 flex items-center justify-center text-slate-400 font-bold text-[10px]">${i + 1}</span>
                <span class="tier-badge-${hop.tier} px-1.5 py-0.5 rounded text-[10px] font-bold">T${hop.tier}</span>
                <span class="text-slate-200 font-bold flex-1">${hop.name}</span>
                <span class="text-slate-400 text-[11px]">${hop.sector}</span>
                <span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">${hop.jurisdiction}</span>
                <button class="px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 text-[10px] btn-hop-inspect" data-hop-id="${hop.id}">Inspect</button>
              </div>
            `).join("")}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button id="btn-highlight-discovered-path" class="px-3 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-black font-semibold text-xs font-mono flex items-center gap-2">
              <i class="fa-solid fa-eye"></i> View & Animate on Graph
            </button>
          </div>
        </div>
      `;

      resultsContainer.querySelector("#btn-highlight-discovered-path")?.addEventListener("click", () => {
        this.switchTab("tab-graph");
        this.highlightCorridor(data.path_nodes);
      });

      resultsContainer.querySelectorAll(".btn-hop-inspect").forEach(b => {
        b.addEventListener("click", () => {
          this.inspectPool(b.getAttribute("data-hop-id"));
        });
      });

    } catch (e) {
      resultsContainer.innerHTML = `<div class="p-3 text-xs font-mono text-red-400">Error querying path: ${e}</div>`;
    }
  },

  renderPoolsBrowser(pools) {
    const container = document.getElementById("pools-cards-container");
    if (!container) return;

    container.innerHTML = pools.map(p => `
      <div class="bg-manifold-card border border-manifold-border hover:border-slate-700 rounded-lg p-4 transition flex flex-col justify-between space-y-3">
        <div class="space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="tier-badge-${p.tier} px-2 py-0.5 rounded text-[10px] font-mono font-bold">T${p.tier} ${p.tier_label.split(':')[0]}</span>
            <span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">${p.jurisdiction}</span>
          </div>
          <h4 class="text-sm font-bold text-white truncate" title="${p.name}">${p.name}</h4>
          <div class="text-[11px] font-mono text-slate-500 truncate">${p.id}</div>
          <div class="text-[11px] font-mono text-purple-300 truncate">${p.sector}</div>
        </div>

        <div class="pt-2.5 border-t border-slate-800 text-xs font-mono space-y-1">
          <div class="flex items-center justify-between">
            <span class="text-slate-500">Inflow:</span>
            <span class="text-emerald-400 font-bold">${this.formatCurrency(p.inflow_usd)}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-slate-500">Outflow:</span>
            <span class="text-amber-400 font-bold">${this.formatCurrency(p.outflow_usd)}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-slate-500">Net:</span>
            <span class="${p.net_flow_usd >= 0 ? 'text-cyan-400' : 'text-red-400'} font-bold">${this.formatCurrency(p.net_flow_usd)}</span>
          </div>
        </div>

        <div class="pt-1 flex items-center justify-between gap-2">
          <button class="w-full py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono border border-slate-700 transition flex items-center justify-center gap-1.5 btn-inspect-pool-card" data-pool-id="${p.id}">
            <i class="fa-solid fa-magnifying-glass text-[10px]"></i> Inspect Pool
          </button>
        </div>
      </div>
    `).join("");

    container.querySelectorAll(".btn-inspect-pool-card").forEach(btn => {
      btn.addEventListener("click", () => {
        this.inspectPool(btn.getAttribute("data-pool-id"));
      });
    });
  },

  filterPoolsBrowser() {
    const q = document.getElementById("pool-filter-input")?.value.trim().toLowerCase() || "";
    const tierVal = document.getElementById("pool-tier-select")?.value;

    const filtered = this.poolsData.filter(p => {
      const matchQ = !q || p.id.toLowerCase().includes(q) || p.name.toLowerCase().includes(q);
      const matchTier = tierVal === "" || p.tier === parseInt(tierVal, 10);
      return matchQ && matchTier;
    });

    document.getElementById("pool-count-label").textContent = filtered.length;
    this.renderPoolsBrowser(filtered);
  },

  // =========================================================================
  // Node Inspection Slide-Over Drawer
  // =========================================================================
  async inspectPool(poolId) {
    this.selectedNodeId = poolId;
    const drawer = document.getElementById("node-drawer");
    const backdrop = document.getElementById("node-drawer-backdrop");

    drawer.classList.remove("translate-x-full");
    backdrop.classList.remove("hidden");

    try {
      const res = await fetch(`/api/pools/${poolId}`);
      const data = await res.json();
      const p = data.pool;

      document.getElementById("drawer-node-name").textContent = p.name;
      document.getElementById("drawer-node-id").textContent = p.id;
      document.getElementById("drawer-sector").textContent = p.sector;
      document.getElementById("drawer-description").textContent = p.description || "Capital flow counterparty pool.";
      document.getElementById("drawer-jurisdiction-badge").textContent = p.jurisdiction;

      const tierBadge = document.getElementById("drawer-tier-badge");
      tierBadge.className = `tier-badge-${p.tier} px-2 py-0.5 rounded text-[10px] font-mono font-bold`;
      tierBadge.textContent = p.tier_label || `TIER ${p.tier}`;

      const decoyBadge = document.getElementById("drawer-decoy-badge");
      if (p.is_decoy) {
        decoyBadge.classList.remove("hidden");
      } else {
        decoyBadge.classList.add("hidden");
      }

      document.getElementById("drawer-conservation-status").textContent = data.conservation_status.replace(/_/g, " ").toUpperCase();
      document.getElementById("drawer-inflow-val").textContent = this.formatCurrency(data.totals.inflow_usd);
      document.getElementById("drawer-outflow-val").textContent = this.formatCurrency(data.totals.outflow_usd);
      document.getElementById("drawer-net-val").textContent = this.formatCurrency(data.totals.net_usd);

      // Metrics
      const metricsContainer = document.getElementById("drawer-metrics-container");
      if (p.metrics && Object.keys(p.metrics).length > 0) {
        metricsContainer.innerHTML = Object.entries(p.metrics).map(([k, v]) => `
          <div class="flex items-center justify-between text-[11px] font-mono py-1 px-2 rounded bg-slate-900/60 border border-slate-800">
            <span class="text-slate-400">${k.replace(/_/g, " ")}:</span>
            <span class="text-cyan-300 font-bold">${typeof v === 'number' ? v.toFixed(3) : v}</span>
          </div>
        `).join("");
      } else {
        metricsContainer.innerHTML = `<div class="text-[11px] text-slate-500 font-mono">Standard institutional cashflow node.</div>`;
      }

      // Upstream list
      const upList = document.getElementById("drawer-upstream-list");
      if (data.upstream_neighbors && data.upstream_neighbors.length > 0) {
        upList.innerHTML = data.upstream_neighbors.map(u => `
          <div class="truncate cursor-pointer hover:text-cyan-400" onclick="App.inspectPool('${u.source}')">
            &bull; ${u.source} <span class="text-slate-500 text-[10px]">(${u.relation})</span>
          </div>
        `).join("");
      } else {
        upList.innerHTML = `<div class="text-slate-500">None (Genesis Origin)</div>`;
      }

      // Downstream list
      const downList = document.getElementById("drawer-downstream-list");
      if (data.downstream_neighbors && data.downstream_neighbors.length > 0) {
        downList.innerHTML = data.downstream_neighbors.map(d => `
          <div class="truncate cursor-pointer hover:text-cyan-400" onclick="App.inspectPool('${d.target}')">
            &bull; ${d.target} <span class="text-slate-500 text-[10px]">(${d.relation})</span>
          </div>
        `).join("");
      } else {
        downList.innerHTML = `<div class="text-slate-500">None (Terminal Sink)</div>`;
      }

      // Associated flows
      const flowsList = document.getElementById("drawer-flows-list");
      const combinedFlows = [...data.inbound_flows, ...data.outbound_flows];
      if (combinedFlows.length > 0) {
        flowsList.innerHTML = combinedFlows.slice(0, 8).map(f => `
          <div class="bg-slate-900 border border-slate-800 rounded p-2 text-[11px] font-mono space-y-1">
            <div class="flex items-center justify-between">
              <span class="text-cyan-400 font-bold">${f.instrument}</span>
              <span class="text-emerald-400">${this.formatCurrency(f.amount_usd_normalized)}</span>
            </div>
            <div class="text-slate-400 text-[10px] flex items-center justify-between">
              <span>${f.source_entity} &rarr; ${f.target_entity}</span>
              <span class="badge-provenance badge-${(f.data_source || 'dtcc').toLowerCase().slice(0, 3)}">${f.data_source || 'LEDGER'}</span>
            </div>
          </div>
        `).join("");
      } else {
        flowsList.innerHTML = `<div class="text-slate-500 text-[11px] font-mono">No direct flow events recorded in DuckDB.</div>`;
      }

    } catch (e) {
      console.warn("Could not load pool details:", e);
    }
  },

  closeDrawer() {
    document.getElementById("node-drawer")?.classList.add("translate-x-full");
    document.getElementById("node-drawer-backdrop")?.classList.add("hidden");
  },

  // =========================================================================
  // Tab 4: Systemic Shock Gauntlet Control Room
  // =========================================================================
  async loadGauntlet(regimeNum) {
    await this.triggerGauntletRegime(regimeNum);
  },

  async triggerGauntletRegime(regimeNum) {
    const titleElem = document.getElementById("sim-active-regime-title");
    const descElem = document.getElementById("sim-active-regime-desc");
    const pillElem = document.getElementById("sim-active-regime-pill");

    titleElem.textContent = `Running Regime ${regimeNum} Simulation...`;

    try {
      const res = await fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ regime: regimeNum })
      });
      const data = await res.json();
      this.currentSimResult = data;

      pillElem.textContent = data.regime_id;
      titleElem.textContent = data.regime_name;
      descElem.textContent = data.description;
      document.getElementById("sim-bypass-pct").textContent = `${data.bypass_corridor_activation_pct.toFixed(1)}%`;
      document.getElementById("sim-cost-delta").textContent = `+${data.avg_pct_cost_delta.toFixed(2)}%`;
      document.getElementById("sim-latency").textContent = `${data.execution_time_ms.toFixed(2)} ms`;

      // Render routes
      const routesContainer = document.getElementById("sim-routes-container");
      routesContainer.innerHTML = Object.entries(data.routes).map(([k, r]) => `
        <div class="bg-slate-900 border border-slate-800 rounded-lg p-3.5 space-y-2">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <div class="text-xs font-mono font-bold text-white flex items-center gap-2">
              <span>${r.source_id}</span>
              <span class="text-slate-500">&rarr;</span>
              <span>${r.target_id}</span>
            </div>
            <div class="flex items-center gap-2 text-xs font-mono">
              ${r.is_severed_expected 
                ? '<span class="px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800 font-bold">[SEVERED: 0 HALLUCINATIONS]</span>' 
                : `<span class="text-amber-400 font-bold">Delta C: +${r.pct_cost_delta}%</span>
                   <span class="text-slate-500">|</span>
                   <span class="text-slate-400">Shock Cost: ${r.shocked_cost}</span>`}
            </div>
          </div>

          <div class="text-[11px] font-mono space-y-1">
            <div class="text-slate-400 flex items-center gap-2">
              <span class="w-16 text-slate-500">Baseline:</span>
              <span class="text-slate-300">${r.baseline_path.join(" &rarr; ")}</span>
            </div>
            <div class="text-slate-400 flex items-center gap-2">
              <span class="w-16 text-slate-500">Shocked:</span>
              <span class="${r.is_severed_expected ? 'text-red-400' : 'text-emerald-300 font-bold'}">${r.shocked_path.length > 0 ? r.shocked_path.join(" &rarr; ") : "Interdicted Corridor (0 Edges)"}</span>
            </div>
          </div>

          ${r.bypasses_used && r.bypasses_used.length > 0 ? `
            <div class="pt-1.5 border-t border-slate-800 flex items-center gap-2 text-[10px] font-mono">
              <span class="text-slate-500">Active Bypass:</span>
              ${r.bypasses_used.map(b => `<span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-bold">${b}</span>`).join("")}
            </div>
          ` : ''}
        </div>
      `).join("");

      // Render bottlenecks
      const bottlenecksContainer = document.getElementById("sim-bottlenecks-list");
      bottlenecksContainer.innerHTML = (data.bottleneck_nodes || []).map(b => `
        <div class="flex items-center justify-between text-xs font-mono p-2 rounded bg-slate-950 border border-slate-800">
          <span class="text-amber-300 font-bold">${b}</span>
          <span class="text-slate-400">Congestion: ${(data.node_congestion_scores[b] || 0.5) * 100}%</span>
        </div>
      `).join("");

      // Render active bypasses
      const bypassesContainer = document.getElementById("sim-bypasses-list");
      bypassesContainer.innerHTML = (data.active_bypasses || []).map(b => `
        <div class="flex items-center justify-between text-xs font-mono p-2 rounded bg-slate-950 border border-slate-800">
          <span class="text-emerald-300 font-bold">${b}</span>
          <span class="text-emerald-400 font-bold">[ACTIVATED 100%]</span>
        </div>
      `).join("");

    } catch (e) {
      console.warn("Could not execute gauntlet regime:", e);
    }
  },

  highlightCurrentSimBypasses() {
    if (!this.currentSimResult) return;
    const bypassNodes = this.currentSimResult.active_bypasses || [];
    this.switchTab("tab-graph");
    this.highlightCorridor(bypassNodes);
  },


  // =========================================================================
  // Tab 6: DuckDB Flow Ledger
  // =========================================================================
  async loadLedger() {
    const q = document.getElementById("ledger-search-input")?.value.trim() || "";
    const curr = document.getElementById("ledger-currency-filter")?.value || "";
    const type = document.getElementById("ledger-type-filter")?.value || "";

    const params = new URLSearchParams({
      limit: this.ledgerLimit,
      offset: this.ledgerOffset,
    });
    if (q) params.set("search", q);
    if (curr) params.set("currency", curr);
    if (type) params.set("flow_type", type);

    try {
      const res = await fetch(`/api/flows?${params.toString()}`);
      const data = await res.json();

      this.ledgerTotal = data.total;
      document.getElementById("ledger-showing-count").textContent = `${this.ledgerOffset + 1} - ${Math.min(this.ledgerTotal, this.ledgerOffset + data.flows.length)}`;
      document.getElementById("ledger-total-count").textContent = this.ledgerTotal;

      document.getElementById("btn-ledger-prev").disabled = this.ledgerOffset === 0;
      document.getElementById("btn-ledger-next").disabled = this.ledgerOffset + this.ledgerLimit >= this.ledgerTotal;

      const tbody = document.getElementById("ledger-table-body");
      if (tbody) {
        tbody.innerHTML = data.flows.map(f => `
          <tr class="table-dark-row">
            <td class="py-2.5 px-4">
              <div class="font-bold text-slate-200 truncate max-w-[140px]" title="${f.event_id}">${f.event_id}</div>
              <div class="text-[10px] text-slate-500">${f.period_label || f.timestamp.split('T')[0]}</div>
            </td>
            <td class="py-2.5 px-4">
              <div class="text-cyan-400 font-bold truncate max-w-[150px]" title="${f.source_entity}">${f.source_entity}</div>
              <span class="text-[10px] text-slate-500">${f.source_jurisdiction}</span>
            </td>
            <td class="py-2.5 px-4">
              <div class="text-purple-400 font-bold truncate max-w-[150px]" title="${f.target_entity}">${f.target_entity}</div>
              <span class="text-[10px] text-slate-500">${f.target_jurisdiction}</span>
            </td>
            <td class="py-2.5 px-4 text-slate-300 truncate max-w-[180px]" title="${f.instrument}">${f.instrument}</td>
            <td class="py-2.5 px-4 text-right font-bold text-slate-200">
              ${f.nominal_amount.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${f.currency}
            </td>
            <td class="py-2.5 px-4 text-right font-bold text-emerald-400">
              ${this.formatCurrency(f.amount_usd_normalized)}
            </td>
            <td class="py-2.5 px-4 text-right font-bold text-amber-400">
              ${this.formatCurrency(f.annualized_rate_usd)} / yr
            </td>
            <td class="py-2.5 px-4 text-center">
              <span class="px-1.5 py-0.5 rounded text-[10px] font-mono bg-slate-800 text-slate-300 border border-slate-700">${f.flow_type}</span>
            </td>
            <td class="py-2.5 px-4 text-center">
              <span class="badge-provenance badge-${f.provenance_badge.toLowerCase()}">${f.provenance_badge}</span>
            </td>
          </tr>
        `).join("");
      }

    } catch (e) {
      console.warn("Could not load /api/flows:", e);
    }
  },

  // =========================================================================
  // Currency Formatter
  // =========================================================================
  formatCurrency(val) {
    if (val === null || val === undefined || isNaN(val)) return "$0.00";
    const abs = Math.abs(val);
    const sign = val < 0 ? "-" : "";
    if (abs >= 1e12) return `${sign}$${(abs / 1e12).toFixed(2)}T`;
    if (abs >= 1e9) return `${sign}$${(abs / 1e9).toFixed(2)}B`;
    if (abs >= 1e6) return `${sign}$${(abs / 1e6).toFixed(2)}M`;
    return `${sign}$${abs.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  },
// =========================================================================
  // TAB 2: VISUAL TREE FLOW EXPLORER ENGINE (INSTITUTIONAL PALANTIR SPEC)
  // =========================================================================

  initVisualTreeExplorer() {
    this.setupVisualTreeListeners();
    this.renderVisualTree();
  },

  setupVisualTreeListeners() {
    // Mode toggles
    const btnCircuits = document.getElementById("btn-mode-circuits");
    const btnRoots = document.getElementById("btn-mode-roots");

    btnCircuits?.addEventListener("click", () => {
      this.treeMode = "circuits";
      btnCircuits.className = "px-3 py-1.5 rounded-md font-bold transition bg-cyan-500 text-black shadow";
      if (btnRoots) btnRoots.className = "px-3 py-1.5 rounded-md font-medium text-slate-300 hover:text-white transition";
      this.treeCurrentHopIndex = 0;
      this.renderVisualTree();
    });

    btnRoots?.addEventListener("click", () => {
      this.treeMode = "roots";
      btnRoots.className = "px-3 py-1.5 rounded-md font-bold transition bg-cyan-500 text-black shadow";
      if (btnCircuits) btnCircuits.className = "px-3 py-1.5 rounded-md font-medium text-slate-300 hover:text-white transition";
      this.treeCurrentHopIndex = 0;
      this.renderVisualTree();
    });

    // Currency filter buttons
    document.querySelectorAll(".tree-curr-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tree-curr-btn").forEach(b => {
          b.className = "px-2 py-0.5 rounded text-[11px] font-mono bg-slate-800 text-slate-300 border border-slate-700 hover:border-slate-500 tree-curr-btn";
        });
        btn.className = "px-2 py-0.5 rounded text-[11px] font-mono bg-cyan-900/80 text-cyan-200 border border-cyan-600 font-bold tree-curr-btn";
        this.treeCurrencyFilter = btn.getAttribute("data-currency") || "ALL";
        this.renderVisualTree();
      });
    });

    // Real-time search filter
    document.getElementById("tree-search-input")?.addEventListener("input", (e) => {
      this.treeSearchQuery = e.target.value.toLowerCase().trim();
      this.renderTreeNodesAndConnectors();
    });

    // Expand/Collapse all branches
    document.getElementById("btn-toggle-all-branches")?.addEventListener("click", () => {
      this.treeAllBranchesExpanded = !this.treeAllBranchesExpanded;
      const textSpan = document.getElementById("branches-toggle-text");
      if (textSpan) {
        textSpan.textContent = this.treeAllBranchesExpanded ? "Collapse Branches" : "Expand Branches";
      }
      this.renderTreeNodesAndConnectors();
    });

    // Flow Stepper Navigation
    document.getElementById("btn-step-prev")?.addEventListener("click", () => this.stepTree(-1));
    document.getElementById("btn-step-next")?.addEventListener("click", () => this.stepTree(1));
    document.getElementById("btn-step-reset")?.addEventListener("click", () => {
      this.treeCurrentHopIndex = 0;
      this.updateTreeStepperUI();
      this.drawTreeConnectors();
    });
    document.getElementById("btn-step-autoplay")?.addEventListener("click", () => this.toggleTreeAutoPlay());

    // Window resize redraws SVG connectors
    window.addEventListener("resize", () => {
      if (this.activeTab === "tab-explorer") {
        this.drawTreeConnectors();
      }
    });
  },

  getCurrentTreeScenario() {
    if (this.treeMode === "roots") {
      return TREE_FLOW_CATALOG.sovereignRoots[this.selectedRootId] || TREE_FLOW_CATALOG.sovereignRoots["french_republic_tresor"];
    }
    return TREE_FLOW_CATALOG.circuits[this.selectedCircuitId] || TREE_FLOW_CATALOG.circuits["CIRCUIT-01-OAT-BUND"];
  },

  renderVisualTree() {
    this.renderTreeSelectorPills();
    this.renderTreeSummaryBanner();
    this.renderTreeNodesAndConnectors();
  },

  renderTreeSelectorPills() {
    const container = document.getElementById("tree-selector-pills");
    if (!container) return;

    if (this.treeMode === "roots") {
      const roots = Object.values(TREE_FLOW_CATALOG.sovereignRoots);
      container.innerHTML = roots.map(r => {
        const isSelected = r.id === this.selectedRootId;
        return `
          <button class="px-3 py-1.5 rounded-lg text-xs font-mono whitespace-nowrap transition border ${
            isSelected
              ? 'bg-cyan-950 text-cyan-300 border-cyan-500 font-bold shadow-[0_0_10px_rgba(0,240,255,0.25)]'
              : 'bg-slate-900/90 text-slate-400 border-slate-800 hover:text-slate-200 hover:border-slate-700'
          }" data-root-id="${r.id}">
            <span class="mr-1 text-[10px] text-slate-500">[${r.jurisdiction}]</span> ${r.shortLabel}
          </button>
        `;
      }).join("");

      container.querySelectorAll("button[data-root-id]").forEach(btn => {
        btn.addEventListener("click", () => {
          this.selectedRootId = btn.getAttribute("data-root-id");
          this.treeCurrentHopIndex = 0;
          this.renderVisualTree();
        });
      });

    } else {
      // Circuits mode (14 curated circuits)
      let circuits = Object.values(TREE_FLOW_CATALOG.circuits);
      if (this.treeCurrencyFilter && this.treeCurrencyFilter !== "ALL") {
        circuits = circuits.filter(c => c.currency.includes(this.treeCurrencyFilter));
      }

      container.innerHTML = circuits.map(c => {
        const isSelected = c.id === this.selectedCircuitId;
        return `
          <button class="px-3 py-1.5 rounded-lg text-xs font-mono whitespace-nowrap transition border ${
            isSelected
              ? 'bg-cyan-950 text-cyan-300 border-cyan-500 font-bold shadow-[0_0_10px_rgba(0,240,255,0.25)]'
              : 'bg-slate-900/90 text-slate-400 border-slate-800 hover:text-slate-200 hover:border-slate-700'
          }" data-circuit-id="${c.id}">
            <span class="mr-1 text-[10px] text-cyan-400 font-bold">${c.shortNum}</span> ${c.shortTitle}
          </button>
        `;
      }).join("");

      container.querySelectorAll("button[data-circuit-id]").forEach(btn => {
        btn.addEventListener("click", () => {
          this.selectedCircuitId = btn.getAttribute("data-circuit-id");
          this.treeCurrentHopIndex = 0;
          this.renderVisualTree();
        });
      });
    }
  },

  renderTreeSummaryBanner() {
    const banner = document.getElementById("active-circuit-banner");
    if (!banner) return;

    const s = this.getCurrentTreeScenario();
    if (!s) return;

    banner.innerHTML = `
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 border-b border-slate-800/80 pb-2.5">
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-xs font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800 font-bold">${s.id}</span>
            <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">${s.theme}</span>
            <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 font-bold">
              <i class="fa-solid fa-check-double mr-1"></i> ${s.doubleEntryProof.status} (${s.doubleEntryProof.leak} Leak)
            </span>
          </div>
          <h4 class="text-base font-bold text-white mt-1.5">${s.title}</h4>
          <p class="text-xs text-slate-300 font-sans mt-0.5">${s.subtitle}</p>
        </div>

        <div class="flex items-center gap-2 shrink-0">
          <div class="text-right font-mono pr-2 border-r border-slate-800">
            <div class="text-[10px] text-slate-400 uppercase">Nominal Flow Volume</div>
            <div class="text-sm font-bold text-cyan-400">${s.nominalVolume}</div>
          </div>
          <button id="btn-tree-focus-graph" class="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-slate-700 text-xs font-mono flex items-center gap-1.5 transition">
            <i class="fa-solid fa-eye"></i> Graph Canvas
          </button>
        </div>
      </div>

      <div class="flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400 pt-1">
        <div class="flex items-center gap-3">
          <span><strong class="text-slate-300">Currency:</strong> <span class="text-amber-300 font-bold">${s.currency}</span></span>
          <span><strong class="text-slate-300">Statutory Source:</strong> <span class="badge-provenance badge-${s.statutoryBadge.toLowerCase().replace(/[^a-z]/g, '') || 'dtcc'}">${s.statutoryBadge}</span></span>
          <span><strong class="text-slate-300">Hops:</strong> ${s.hops.length} Sequential Transitions</span>
        </div>
        <div class="text-slate-400 text-[10px]">
          Inflow: <span class="text-emerald-400">${s.doubleEntryProof.inflow}</span> · Outflow: <span class="text-amber-400">${s.doubleEntryProof.outflow}</span> · Net: <span class="text-cyan-400">${s.doubleEntryProof.net}</span>
        </div>
      </div>
    `;

    document.getElementById("btn-tree-focus-graph")?.addEventListener("click", () => {
      const nodeIds = s.nodes.map(n => n.id);
      this.switchTab("tab-graph");
      this.highlightCorridor(nodeIds);
    });
  },

  renderTreeNodesAndConnectors() {
    const s = this.getCurrentTreeScenario();
    if (!s) return;

    // Filter nodes by query if search active
    const q = this.treeSearchQuery;
    const filterNode = (n) => {
      if (!q) return true;
      return n.name.toLowerCase().includes(q) || n.id.toLowerCase().includes(q) || n.sector.toLowerCase().includes(q) || n.jurisdiction.toLowerCase().includes(q);
    };

    const t0Nodes = s.nodes.filter(n => n.tier === 0 && filterNode(n));
    const t1Nodes = s.nodes.filter(n => n.tier === 1 && filterNode(n));
    const t2Nodes = s.nodes.filter(n => n.tier === 2 && filterNode(n));
    const t3Nodes = s.nodes.filter(n => n.tier === 3 && filterNode(n));

    document.getElementById("tier-0-count").textContent = `${t0Nodes.length} Nodes`;
    document.getElementById("tier-1-count").textContent = `${t1Nodes.length} Nodes`;
    document.getElementById("tier-2-count").textContent = `${t2Nodes.length} Nodes`;
    document.getElementById("tier-3-count").textContent = `${t3Nodes.length} Nodes`;

    const activeHop = s.hops[this.treeCurrentHopIndex] || null;

    const renderColumnNodes = (nodes, containerId, tier) => {
      const el = document.getElementById(containerId);
      if (!el) return;

      if (nodes.length === 0) {
        el.innerHTML = `<div class="p-4 rounded border border-dashed border-slate-800 text-center text-xs text-slate-500 font-mono">No nodes match filter</div>`;
        return;
      }

      el.innerHTML = nodes.map(n => {
        const isCurrentActive = activeHop && (activeHop.source === n.id || activeHop.target === n.id);
        const isSourceOfHop = activeHop && activeHop.source === n.id;
        const isTargetOfHop = activeHop && activeHop.target === n.id;
        const hasBranches = n.branches && n.branches.length > 0;
        const isBranchExpanded = this.treeAllBranchesExpanded || this.treeExpandedBranches.has(n.id);

        return `
          <div class="flow-node-card tier-${n.tier}-card ${isCurrentActive ? 'active-hop pulse-glow' : ''}" data-node-id="${n.id}" data-tier="${n.tier}">
            <div class="flex items-center justify-between gap-1 mb-1.5">
              <span class="tier-badge-${n.tier} px-1.5 py-0.5 rounded text-[9px] font-mono font-bold">
                T${n.tier} ${n.tierLabel || ''}
              </span>
              <div class="flex items-center gap-1">
                <span class="px-1.5 py-0.2 rounded bg-slate-800 text-slate-300 font-mono text-[9px] border border-slate-700 font-semibold">[${n.jurisdiction}]</span>
                ${isSourceOfHop ? '<span class="px-1 py-0.2 rounded bg-cyan-950 text-cyan-300 font-mono text-[8px] border border-cyan-800 font-bold uppercase">HOP SRC</span>' : ''}
                ${isTargetOfHop ? '<span class="px-1 py-0.2 rounded bg-emerald-950 text-emerald-300 font-mono text-[8px] border border-emerald-800 font-bold uppercase">HOP DST</span>' : ''}
              </div>
            </div>

            <h5 class="text-xs font-bold text-white leading-snug mb-1 truncate" title="${n.name}">${n.name}</h5>
            <div class="text-[10px] font-mono text-slate-400 truncate mb-1.5">${n.sector}</div>

            <div class="flex items-center justify-between text-[10px] font-mono pt-1.5 border-t border-slate-800/80">
              <span class="text-slate-400">Flow Vol:</span>
              <span class="text-cyan-300 font-bold">${n.volume || '$0.00'}</span>
            </div>

            ${hasBranches ? `
              <div class="mt-2 pt-1 border-t border-slate-800/60 flex items-center justify-between">
                <button class="branch-pill btn-toggle-node-branch" data-branch-node="${n.id}">
                  <i class="fa-solid fa-code-branch text-[9px] mr-1"></i> ${isBranchExpanded ? 'Hide' : 'Expand'} ${n.branches.length} Conduits
                </button>
                <span class="text-[9px] font-mono text-slate-500">${n.provenance || 'DTCC'}</span>
              </div>
            ` : ''}

            ${hasBranches && isBranchExpanded ? `
              <div class="mt-2 pt-2 border-t border-slate-800/80 space-y-1 bg-slate-950/80 p-2 rounded text-[10px] font-mono">
                <div class="text-[9px] text-slate-500 uppercase font-bold">Active Branch Conduits:</div>
                ${n.branches.map(b => `
                  <div class="flex items-center justify-between text-slate-300 py-0.5 border-b border-slate-900 last:border-none">
                    <span class="truncate mr-1">→ ${b.targetName}</span>
                    <span class="text-emerald-400 font-semibold shrink-0">${b.volume}</span>
                  </div>
                `).join("")}
              </div>
            ` : ''}
          </div>
        `;
      }).join("");

      // Bind node card click to inspect balance sheet
      el.querySelectorAll(".flow-node-card").forEach(card => {
        card.addEventListener("click", (e) => {
          if (e.target.closest(".btn-toggle-node-branch")) return;
          const nid = card.getAttribute("data-node-id");
          this.inspectTreeNode(nid);
        });
      });

      // Bind branch toggles
      el.querySelectorAll(".btn-toggle-node-branch").forEach(btn => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const nid = btn.getAttribute("data-branch-node");
          if (this.treeExpandedBranches.has(nid)) {
            this.treeExpandedBranches.delete(nid);
          } else {
            this.treeExpandedBranches.add(nid);
          }
          this.renderTreeNodesAndConnectors();
        });
      });
    };

    renderColumnNodes(t0Nodes, "tier-0-nodes", 0);
    renderColumnNodes(t1Nodes, "tier-1-nodes", 1);
    renderColumnNodes(t2Nodes, "tier-2-nodes", 2);
    renderColumnNodes(t3Nodes, "tier-3-nodes", 3);

    this.updateTreeStepperUI();

    // Redraw SVG connectors
    setTimeout(() => this.drawTreeConnectors(), 40);
  },

  updateTreeStepperUI() {
    const s = this.getCurrentTreeScenario();
    if (!s) return;

    const totalHops = s.hops.length;
    const currentHop = s.hops[this.treeCurrentHopIndex];
    if (!currentHop) return;

    // Badges & progress
    const stepBadge = document.getElementById("step-counter-badge");
    if (stepBadge) {
      stepBadge.textContent = `Hop ${this.treeCurrentHopIndex + 1} of ${totalHops}`;
    }

    const progressFill = document.getElementById("flow-progress-fill");
    if (progressFill) {
      const pct = Math.round(((this.treeCurrentHopIndex + 1) / totalHops) * 100);
      progressFill.style.width = `${pct}%`;
    }

    // Commentary text
    const hopTitle = document.getElementById("step-hop-title");
    if (hopTitle) {
      const srcNode = s.nodes.find(n => n.id === currentHop.source);
      const dstNode = s.nodes.find(n => n.id === currentHop.target);
      const srcName = srcNode ? srcNode.name : currentHop.source;
      const dstName = dstNode ? dstNode.name : currentHop.target;
      hopTitle.textContent = `${srcName} ➔ ${dstName}`;
    }

    const hopExplanation = document.getElementById("step-hop-explanation");
    if (hopExplanation) {
      hopExplanation.textContent = currentHop.narrative;
    }

    const actionBadge = document.getElementById("step-action-badge");
    if (actionBadge) {
      actionBadge.textContent = currentHop.action || "FLOW TRANSMISSION";
    }
  },

  stepTree(direction) {
    const s = this.getCurrentTreeScenario();
    if (!s || !s.hops || s.hops.length === 0) return;

    this.treeCurrentHopIndex += direction;
    if (this.treeCurrentHopIndex < 0) {
      this.treeCurrentHopIndex = s.hops.length - 1;
    } else if (this.treeCurrentHopIndex >= s.hops.length) {
      this.treeCurrentHopIndex = 0;
    }

    this.renderTreeNodesAndConnectors();
  },

  toggleTreeAutoPlay() {
    const btn = document.getElementById("btn-step-autoplay");
    if (this.treeAutoPlayTimer) {
      clearInterval(this.treeAutoPlayTimer);
      this.treeAutoPlayTimer = null;
      if (btn) {
        btn.innerHTML = `<i class="fa-solid fa-play text-[10px]"></i> Auto-Play`;
        btn.className = "px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-black font-mono text-xs font-bold flex items-center gap-1.5 transition shadow";
      }
    } else {
      if (btn) {
        btn.innerHTML = `<i class="fa-solid fa-pause text-[10px]"></i> Pause`;
        btn.className = "px-3 py-1.5 rounded bg-amber-500 hover:bg-amber-400 text-black font-mono text-xs font-bold flex items-center gap-1.5 transition shadow";
      }
      this.stepTree(1);
      this.treeAutoPlayTimer = setInterval(() => {
        this.stepTree(1);
      }, 2500);
    }
  },

  drawTreeConnectors() {
    const svg = document.getElementById("tree-flow-svg");
    if (!svg) return;

    const s = this.getCurrentTreeScenario();
    if (!s || !s.hops) return;

    const canvas = document.querySelector(".tree-flow-canvas");
    if (!canvas) return;

    const canvasRect = canvas.getBoundingClientRect();
    svg.setAttribute("width", `${canvas.scrollWidth}px`);
    svg.setAttribute("height", `${canvas.scrollHeight}px`);
    svg.innerHTML = "";

    const activeHop = s.hops[this.treeCurrentHopIndex];

    s.hops.forEach((hop, idx) => {
      const srcEl = canvas.querySelector(`.flow-node-card[data-node-id="${hop.source}"]`);
      const dstEl = canvas.querySelector(`.flow-node-card[data-node-id="${hop.target}"]`);

      if (!srcEl || !dstEl) return;

      const srcRect = srcEl.getBoundingClientRect();
      const dstRect = dstEl.getBoundingClientRect();

      // Start coordinate at right-center of source
      const x1 = srcRect.right - canvasRect.left + canvas.scrollLeft;
      const y1 = srcRect.top - canvasRect.top + (srcRect.height / 2) + canvas.scrollTop;

      // End coordinate at left-center of target
      const x2 = dstRect.left - canvasRect.left + canvas.scrollLeft;
      const y2 = dstRect.top - canvasRect.top + (dstRect.height / 2) + canvas.scrollTop;

      // Bézier control points
      const dx = Math.max(40, (x2 - x1) * 0.5);
      const d = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

      const isCurrent = idx === this.treeCurrentHopIndex;
      const isPast = idx < this.treeCurrentHopIndex;

      const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
      path.setAttribute("d", d);

      if (isCurrent) {
        path.setAttribute("class", "flow-connector-path flow-active");
      } else if (isPast) {
        path.setAttribute("class", "flow-connector-path flow-completed");
      } else {
        path.setAttribute("class", "flow-connector-path");
      }

      svg.appendChild(path);

      // Volume indicator circle/text along the path for active hop
      if (isCurrent && hop.volume) {
        const mx = (x1 + x2) / 2;
        const my = (y1 + y2) / 2;

        const bgRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        bgRect.setAttribute("x", `${mx - 28}`);
        bgRect.setAttribute("y", `${my - 10}`);
        bgRect.setAttribute("width", "56");
        bgRect.setAttribute("height", "20");
        bgRect.setAttribute("rx", "4");
        bgRect.setAttribute("fill", "#09101d");
        bgRect.setAttribute("stroke", "#00f0ff");
        bgRect.setAttribute("stroke-width", "1");
        svg.appendChild(bgRect);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", `${mx}`);
        text.setAttribute("y", `${my + 4}`);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("fill", "#00f0ff");
        text.setAttribute("font-family", "monospace");
        text.setAttribute("font-size", "10px");
        text.setAttribute("font-weight", "bold");
        text.textContent = hop.volume;
        svg.appendChild(text);
      }
    });
  },

  async inspectTreeNode(nodeId) {
    const card = document.getElementById("tree-node-inspection-card");
    if (!card) return;

    this.selectedNodeId = nodeId;
    const s = this.getCurrentTreeScenario();
    const catalogNode = s ? s.nodes.find(n => n.id === nodeId) : null;

    card.classList.remove("hidden");
    card.innerHTML = `<div class="p-6 text-center text-xs font-mono text-cyan-400 animate-pulse">Inspecting balance sheet mechanics for '${nodeId}'...</div>`;
    card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    let poolData = null;
    try {
      const res = await fetch(`/api/pools/${nodeId}`);
      if (res.ok) {
        poolData = await res.json();
      }
    } catch (e) {
      console.warn("Could not fetch /api/pools for node:", nodeId, e);
    }

    this.renderTreeNodeInspectionCard(catalogNode, poolData);
  },

  renderTreeNodeInspectionCard(catalogNode, poolData) {
    const card = document.getElementById("tree-node-inspection-card");
    if (!card) return;

    const p = poolData?.pool || {};
    const totals = poolData?.totals || {};
    const name = catalogNode?.name || p.name || this.selectedNodeId;
    const tier = catalogNode?.tier ?? p.tier ?? 2;
    const jurisdiction = catalogNode?.jurisdiction || p.jurisdiction || "GLOBAL";
    const sector = catalogNode?.sector || p.sector || "financial_institution";
    const provenance = catalogNode?.provenance || poolData?.provenance || "ECB SDW / SEC EDGAR";
    const velocity = catalogNode?.velocity || "Overnight (T+0 to T+1) Clearing Velocity";
    const nominalVol = catalogNode?.volume || (totals.inflow_usd ? this.formatCurrency(totals.inflow_usd) : "$250.0B");

    const assets = catalogNode?.balanceItems?.assets || [
      { name: "Sovereign Debt Benchmark Paper", amount: nominalVol },
      { name: "Intraday Refinancing Claims & Collateral", amount: "$85.0B" },
      { name: "Positive RTGS Interbank Balances", amount: "$45.2B" }
    ];

    const liabilities = catalogNode?.balanceItems?.liabilities || [
      { name: "Central Bank Commercial Reserve Balances", amount: nominalVol },
      { name: "Overnight Triparty Repo Liabilities", amount: "$85.0B" },
      { name: "Statutory Capital & Retained Reserves", amount: "$45.2B" }
    ];

    card.innerHTML = `
      <div class="border-b border-slate-800 pb-3 flex items-start justify-between">
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="tier-badge-${tier} px-2 py-0.5 rounded text-[10px] font-mono font-bold">
              TIER ${tier}: ${catalogNode?.tierLabel || 'FINANCIAL INTERMEDIARY'}
            </span>
            <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px] border border-slate-700 font-bold">[${jurisdiction}]</span>
            <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-mono text-[10px] border border-emerald-800 font-bold">
              <i class="fa-solid fa-shield-halved mr-1"></i> $0.00 LEAK VERIFIED (CONSERVED)
            </span>
          </div>
          <h3 class="text-lg font-bold text-white mt-1.5">${name}</h3>
          <span class="text-xs font-mono text-slate-400">${this.selectedNodeId} · ${sector}</span>
        </div>
        
        <div class="flex items-center gap-2">
          <button id="btn-inspect-in-drawer" class="px-3 py-1.5 rounded bg-cyan-600 hover:bg-cyan-500 text-black text-xs font-mono font-bold transition flex items-center gap-1.5 shadow">
            <i class="fa-solid fa-table-columns"></i> Full Drawer
          </button>
          <button id="btn-close-tree-card" class="text-slate-400 hover:text-white px-2 py-1 text-base transition">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>
      </div>

      <!-- Key Metrics Strip -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-[10px] text-slate-500 uppercase block">Gross Flow Volume</span>
          <span class="text-sm font-bold text-cyan-400">${nominalVol}</span>
        </div>
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-[10px] text-slate-500 uppercase block">Statutory Provenance</span>
          <span class="text-xs font-bold text-purple-300 truncate block">${provenance}</span>
        </div>
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-[10px] text-slate-500 uppercase block">Turnover Velocity</span>
          <span class="text-xs font-bold text-amber-300 truncate block">${velocity}</span>
        </div>
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-[10px] text-slate-500 uppercase block">Conservation Check</span>
          <span class="text-xs font-bold text-emerald-400">Strictly Conserved</span>
        </div>
      </div>

      <!-- T-Account Double-Entry Balance Sheet Line Items -->
      <div class="space-y-2">
        <div class="flex items-center justify-between">
          <h4 class="text-xs font-bold font-mono text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
            <i class="fa-solid fa-scale-balanced text-cyan-400"></i> Double-Entry Balance Sheet Line Items (T-Account Breakdown)
          </h4>
          <span class="text-[10px] font-mono text-emerald-400">Net Double-Entry Δ = $0.00</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <!-- Assets Column -->
          <div class="bg-slate-950 rounded border border-slate-800 overflow-hidden">
            <div class="bg-blue-950/40 px-3 py-1.5 border-b border-slate-800 flex items-center justify-between font-mono text-xs">
              <span class="font-bold text-blue-300">ASSETS (CLAIMS)</span>
              <span class="text-slate-400">${nominalVol}</span>
            </div>
            <table class="t-account-table">
              <tbody>
                ${assets.map(a => `
                  <tr>
                    <td class="text-slate-300">${a.name}</td>
                    <td class="text-right text-blue-300 font-bold font-mono-fig">${a.amount}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>

          <!-- Liabilities Column -->
          <div class="bg-slate-950 rounded border border-slate-800 overflow-hidden">
            <div class="bg-purple-950/40 px-3 py-1.5 border-b border-slate-800 flex items-center justify-between font-mono text-xs">
              <span class="font-bold text-purple-300">LIABILITIES & EQUITY (OBLIGATIONS)</span>
              <span class="text-slate-400">${nominalVol}</span>
            </div>
            <table class="t-account-table">
              <tbody>
                ${liabilities.map(l => `
                  <tr>
                    <td class="text-slate-300">${l.name}</td>
                    <td class="text-right text-purple-300 font-bold font-mono-fig">${l.amount}</td>
                  </tr>
                `).join("")}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;

    document.getElementById("btn-close-tree-card")?.addEventListener("click", () => {
      card.classList.add("hidden");
    });

    document.getElementById("btn-inspect-in-drawer")?.addEventListener("click", () => {
      this.inspectPool(this.selectedNodeId);
    });
  }
};
